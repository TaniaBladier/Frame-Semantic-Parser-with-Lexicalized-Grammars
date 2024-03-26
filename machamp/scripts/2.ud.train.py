import os
from allennlp.common import Params
import myutils

if not os.path.isdir('configs/tmp/'):
    os.mkdir('configs/tmp/')

data_configs = []
## single-dataset models
for udPath in ['data/ud-treebanks-v' + myutils.UDversion + '.singleToken/', 'data/ud-treebanks-v2.extras.singleToken/']:
    for UDdir in os.listdir(udPath):
        if not UDdir.startswith("UD") or not os.path.isdir(udPath + UDdir):
            continue
        train, dev, test = myutils.getTrainDevTest(udPath + UDdir)
        
        if train != '':
            for embedding in ['mbert', 'rembert', 'xlmr']:
                if not myutils.hasColumn(train, 1, threshold=.1):
                    #print('noWords ', train)
                    continue
                config = {}
                config['train_data_path'] = train
                if dev != '':
                    config['validation_data_path'] = dev
                config['word_idx'] = 1
                config['tasks'] = {}
                if myutils.hasColumn(train, 3, threshold=.1):
                    config['tasks']['upos'] = {'task_type':'seq', 'column_idx':3}
                if myutils.hasColumn(train, 2, threshold=.95):
                    config['tasks']['lemma'] = {'task_type':'string2string', 'column_idx':2}
                if myutils.hasColumn(train, 5, threshold=.95):
                    config['tasks']['feats'] = {'task_type':'seq', 'column_idx':5}
                config['tasks']['dependency'] = {'task_type':'dependency', 'column_idx':6}
            
                allennlpConfig = Params({UDdir: config})
                jsonPath = 'configs/tmp/' + UDdir + '.json'
                data_configs.append(jsonPath)
                allennlpConfig.to_file(jsonPath)
                #paramsConfig = 'configs/params-' + embedding + '.json'
                #for seed in myutils.seeds:
                #    if myutils.getModel(UDdir + '.' + embedding + '.' + seed) == '':
                #        print('python3 train.py --dataset_config ' + jsonPath + ' --seed ' + seed + ' --name ' + UDdir + '.' + embedding + '.' + seed + ' --parameters_config ' + paramsConfig)

def makeParams(mlm):
    paramsPath = 'configs/params.' + mlm.replace('/', '-') + '.json'
    if not os.path.isfile(paramsPath):
        size = myutils.getEmbedSize(mlm)
        outFile = open(paramsPath, 'w')
        outFile.write('local transformer_model = "' + mlm + '";\n')
        outFile.write('local transformer_dim = ' + str(size) + ';\n')
        outFile.write(''.join(open('configs/params.json').readlines()[2:]))
        outFile.close()
    return paramsPath


# multi-dataset models
multiEmbeds = ["microsoft/mdeberta-v3-base", "studio-ousia/mluke-large", "google/rembert", "cardiffnlp/twitter-xlm-roberta-base", "xlm-roberta-large", "bert-base-multilingual-cased", "xlm-roberta-base", 'distilbert-base-multilingual-cased', 'facebook/xlm-roberta-xl']
#TODO not efficient, hasColumn is expensive and done 3 times for each check!
for seed in myutils.seeds:
    for embed in multiEmbeds:
        hyper_params = makeParams(embed)
        name = 'multi-' + embed.replace('/', '-') + '.' + seed
        cmd = 'python3 train.py --dataset_configs ' + ' '.join(data_configs) + ' --parameters_config ' + hyper_params + ' --name ' + name + ' --seed ' + str(seed)
        print(cmd) 

    
    
