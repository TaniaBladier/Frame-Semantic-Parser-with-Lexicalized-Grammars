import os

for modelName in os.listdir('logs'):
    for dateName in os.listdir('logs/' + modelName):
        modelDir = 'logs/' + modelName + '/' + dateName + '/'
        if not os.path.isfile(modelDir + 'model.tar.gz'):
            cmd = 'rm -rf ' + modelDir
            print(cmd)
            os.system(cmd)

for modelName in os.listdir('logs'):
    if len(os.listdir('logs/' + modelName)) == 0:
        cmd = 'rm -rf logs/' + modelName
        print(cmd)
        os.system(cmd)
    else:
        for oldModel in sorted(os.listdir('logs/' + modelName))[:-1]:
            cmd = 'rm -rf logs/' + modelName + '/' + oldModel
            print(cmd)
            os.system(cmd)
        
cmd = 'rm logs/*/*/*th'
print(cmd)
os.system(cmd)
