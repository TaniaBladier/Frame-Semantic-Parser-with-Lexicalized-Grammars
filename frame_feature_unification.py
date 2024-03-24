from nltk.featstruct import FeatStruct
from nltk.sem.logic import Variable 
import ast
from conllu import parse_tree


input_file = 'example_feature_unif_data.txt'



def readFile(path):
    sentences = []
    sentence = []
    for line in open(path, 'r'):
        line = line.rstrip()
        if not line:
            if len(sentence) > 0:
                sentences.append(sentence)
                sentence = []
        else:
            word = line.split("\t")
            sentence.append(word)
    if len(sentence) > 0:
        sentences.append(sentence)
    print("number of sents: ", len(sentences))
    return sentences



def transform_lnkngs_to_frame(fr, token, frame_name, linking):
    fra_na = frame_name[1:-1]
    if frame_name != '[--]' and linking != '[--]':

        linkings = ast.literal_eval(linking)
        lst_of_them_roles = []
        for lnk in linkings:
            srole = lnk[1].lower().replace('-', '') + '=(?I' + str(lnk[0]) + ')'
            lst_of_them_roles.append(srole)
        sent_frame = FeatStruct('[_e' + str(fr) + '="' + fra_na + '", ' + ', '.join(lst_of_them_roles) + ']')
        sent_frame_str = '[_e' + str(fr) + '="' + fra_na + '", ' + ', '.join(lst_of_them_roles) + ']'

        return sent_frame, sent_frame_str
    if frame_name != '[--]' and linking == '[--]':
        entity_frame = FeatStruct('[' + token + ']')
        entity_frame_str = '[' + token + ']'

        return entity_frame, entity_frame_str
    else:
        return '_', '_'


def pparse_to_conll(pparse_str):

    pparse_str = pparse_str.strip().replace(":1.0", "")
    conllparse = ''

    for line in pparse_str.split("\n"):
        ls = line.split("\t")

        _, frame_str = transform_lnkngs_to_frame(ls[0], ls[1], ls[6], ls[7])

        new_line = ls[:2] + [ls[4]] +[frame_str] + ['_']*2 + ls[2:]  + ['_']*2 

        conllparse = conllparse + '\t'.join(new_line) + '\n'
    return conllparse


def make_child_list(tree):
    child_list = []

    agenda = list(tree.children)
    while agenda:
        ch = agenda.pop()
        if not ch or len(ch.children) > 0:
            agenda.extend(list(ch.children))
            child_list.append(ch)
                
        else:
            child_list.append(ch)

    return child_list


def make_dep_dict(tree):
    dep_dict = {}
    ch_list = make_child_list(tree) + [tree]
    for ch in ch_list:
        dep_dict[ch.token['id']] = sorted([x.token['id'] for x in make_child_list(ch) if x.token['id'] != ch.token['id']])
    return dep_dict

        
def reformat_featstruct(fst):
    fstring = str(fst)
    new_fstring = fstring.replace('  ', '').replace('\n', '').replace('(', '').replace(')', '').replace("[]", "")
    new_fstring = new_fstring.replace('][', ', ').replace("['", "").replace("']", "")
    return FeatStruct(new_fstring)


def remove_duplicates_preserve_order(lst):
    new_k = []
    for elem in lst:
        if elem not in new_k:
            new_k.append(elem)
    lst = new_k
    return lst



def check_that_subtree_has_subframes(subtree):
    subtree_children = [x for x in make_child_list(subtree)]
    if any(item.token['upostag'].startswith('[_e') for item in subtree_children):# and not '*' in item.token['lemma'] for item in subtree_children):
        return True
    else:
        return False

        
def find_parent(subtree, tree):
    ch_list = remove_duplicates_preserve_order(make_child_list(tree) + [tree])
    for k in ch_list:
        if subtree in k.children:
            return k
                 

def make_list_of_higher_nodes(subtree, wholetree):
    parent_list = []

    agenda = [find_parent(subtree, wholetree)]
    while agenda:
        ch = agenda.pop()
        if find_parent(ch, wholetree):
            agenda.extend([find_parent(ch, wholetree)])
            parent_list.append(find_parent(ch, wholetree))                
        else:
            parent_list.append(ch)
    return parent_list


def subframe_has_parent_frame(subtree, wholetree):
    parent = find_parent(subtree, wholetree)
    if not parent:
        return False
    if parent:
        lst_of_higher_nodes = make_list_of_higher_nodes(subtree, wholetree)
        superframes = [x.token['upostag'] for x in lst_of_higher_nodes if x.token['upostag'].startswith('[_e')]
        if len(superframes) > 0:
            return True
        else:
            return False

            
def make_frame(subtree):
   sent_frame = FeatStruct(subtree.token['upostag'])
   number_of_slots = str(sent_frame).count("?I")
   if "?I0" in str(sent_frame):
       number_of_slots = number_of_slots - 1
   sroles = [x.token['upostag'] for x in subtree.children if x.token['upostag'] != '_']
   if len(sroles) == number_of_slots:
      for i, x in enumerate(sroles, 1):
          sent_frame = sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})        
   return reformat_featstruct(sent_frame)


def make_frame_with_subframes(subtree):
    sent_frame = make_frame(subtree) 
    sroles = []
    fr_new = [x.token['upostag'] for x in subtree.children if (x.token['upostag'] != '_' and not x.token['upostag'].startswith("[_e"))]
    sroles.extend(fr_new)
    for i, x in enumerate(sroles, 1):
        sent_frame = sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})
    return sent_frame

def remove_subtree(subtree, tree):
    tree.children = [x for x in tree.children if x != subtree]
    #tree.print_tree()
    return tree


def delete_e_feature_from_featstruct(pp_frame):
     feat_to_del = ''
     for k in pp_frame.keys():
         if k.startswith("_e"):
             feat_to_del = feat_to_del + k
     del pp_frame[feat_to_del]
     return pp_frame


def combine_frames_from_dep_tree(deptree):

    # start with frames which don't have further subframes
    frame_agenda = [ch for ch in [deptree] + make_child_list(deptree) 
                      if ch.token['upostag'].startswith('[_e') and not check_that_subtree_has_subframes(ch)] 

    frames = []


    while frame_agenda:
        fr = frame_agenda.pop()  

        # if this little frame is part of a bigger frame, 
        # either store it as a separate frame if it is a perifery frame
        # or put it together with the parent onto agenda together with its parent
        # since this frame fills a role in the superframe

        if subframe_has_parent_frame(fr, deptree):
            if "*" in fr.token['lemma'] and not "event" in fr.token['upostag']:
                frames.append(make_frame(fr))
                parent_tree = find_parent(fr, deptree)
                pruned_parent_tree = remove_subtree(fr, parent_tree)
                frame_agenda.append(pruned_parent_tree)
            
            if not "*" in fr.token['lemma'] and not "event" in fr.token['upostag']:
                parent_tree = find_parent(fr, deptree)
                sent_frame = make_frame(parent_tree)
                sroles = []
                fr_new = [FeatStruct(x.token['upostag']) for x in fr.children if (x.token['upostag'] != '_' and not x.token['upostag'].startswith("[_e"))]
                sroles.extend(fr_new)
                for i, x in enumerate(sroles, 1):
                    sent_frame = sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})
                    frames.append(sent_frame)

            # special treatment for modifier PPs
            if "event" in fr.token['upostag'] and "*" in fr.token['lemma']:
                parent_tree = find_parent(fr, deptree)
                sent_frame = make_frame(parent_tree)
                pp_frame = make_frame(fr)
                pp_frame = delete_e_feature_from_featstruct(pp_frame)
                sroles = []
                fr_new = [FeatStruct(x.token['upostag']) for x in fr.children if (x.token['upostag'] != '_' and not x.token['upostag'].startswith("[_e"))]
                sroles.extend(fr_new)
                for i, x in enumerate(sroles, 1):
                    sent_frame = sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})
                    sent_frame = sent_frame.unify(pp_frame)
                    #frames.append(sent_frame)
                if find_parent(parent_tree, deptree):
                    new_p = find_parent(parent_tree, deptree)
                    new_p = remove_subtree(parent_tree, new_p)
                    p_sent_frame = make_frame(new_p)
                    p_sroles = []
                    p_fr_new = [FeatStruct(x.token['upostag']) for x in new_p.children if (x.token['upostag'] != '_' and not x.token['upostag'].startswith("[_e"))]
                    p_sroles.extend([sent_frame])
                    p_sroles.extend(p_fr_new)

                    for i, x in enumerate(p_sroles, 1):
                        p_sent_frame = p_sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})

                    frames.append(p_sent_frame)
                else:
                    frames.append(sent_frame)
            
            # special treatment for attribute PPs
            if "event" in fr.token['upostag'] and not "*" in fr.token['lemma']:
                parent_tree = find_parent(fr, deptree)
                pp_frame = make_frame(fr)
                pp_frame = delete_e_feature_from_featstruct(pp_frame)
                type_pp_frame = [k for k in pp_frame.keys()][0]
                sent_frame = make_frame(parent_tree)
                del sent_frame[type_pp_frame]
                sroles = []
                fr_new = [FeatStruct(x.token['upostag']) for x in fr.children if (x.token['upostag'] != '_' and not x.token['upostag'].startswith("[_e"))]
                sroles.extend(fr_new)
                for i, x in enumerate(sroles, 1):
                    sent_frame = sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})
                    sent_frame = sent_frame.unify(pp_frame)

                if find_parent(parent_tree, deptree):
                    new_p = find_parent(parent_tree, deptree)
                    new_p = remove_subtree(parent_tree, new_p)
                    p_sent_frame = make_frame(new_p)
                    p_sroles = []
                    p_fr_new = [FeatStruct(x.token['upostag']) for x in new_p.children if (x.token['upostag'] != '_' and not x.token['upostag'].startswith("[_e"))]
                    p_sroles.extend([sent_frame])
                    p_sroles.extend(p_fr_new)

                    for i, x in enumerate(p_sroles, 1):
                        p_sent_frame = p_sent_frame.substitute_bindings({Variable('?I'+ str(i)): FeatStruct(x)})

                    frames.append(p_sent_frame)
                else:
                    frames.append(sent_frame)



        # if the frame has no parent, check if it has subframes 
        # if not, it means that there is just one frame in the sentence
        
        # it the frame has a parent, combine it with the tokens from the sentences
        # and put it on the list of semantic roles for the bigger frame
        else:            
            if not check_that_subtree_has_subframes(fr):
                sent_frame = make_frame(fr)
                frames.append(sent_frame)
            else:      
                frame_with_subframes = make_frame_with_subframes(fr)
                frames.append(frame_with_subframes)
    #print(remove_duplicates_preserve_order(frames))
    return remove_duplicates_preserve_order(frames) 



sents = readFile(input_file)




for sent in sents: #[sents[3]]: # sents[1:]: #sents[1:]:  
    
    conll_p = [[w[0], w[1], w[2], w[4], w[6], w[7]] for w in sent]

    conll_parse = pparse_to_conll('\n'.join(['\t'.join(w) for w in sent]))
    dep_tree = parse_tree(conll_parse)
    #dep_tree[0].print_tree()

    resulted_frames = combine_frames_from_dep_tree(dep_tree[0])
    print()
    print()
    print('+++++++++++++++++++')
    print()
    print("SENTENCE: ", " ".join([w[1] for w in sent]))
    print()
    #print()
    #print(conll_p)
    for v in conll_p:
      a,b,c, d, e, f = v
      print ("{:<2} {:<15} {:<2} {:<60} {:<27} {:<15}".format( a, b, c, d, e, f))

    print()

    print("SENTENCE FRAME: ")
    print()
    if isinstance(resulted_frames, list):
      for x in resulted_frames:
        print(x)
        print()
        print()
    else:
      print(resulted_frames)



print()
print()



#############################




"""






print('##############################################################')
i1 = FeatStruct('["sheep"]')
fs1a = FeatStruct('[_E_f0="COME-AFTER_FOLLOW-IN-TIME", agent=(?I2), cotheme=(?I3)]')
i4 = FeatStruct('["him"]')

fsneua = fs1a.substitute_bindings({Variable('?I2'): i1, Variable('?I3'): i4})



print(reformat_featstruct(fsneua))
print()

print('#####')
i1b = FeatStruct('["It"]')
fs1b = FeatStruct('[_E_f0="GUESS", SUBJ=(?I2), agent=(?I2), theme=(?I3)]')
fs2b = FeatStruct('[_E_f1="OBTAIN", SUBJ=(?I0), agent=(?I0), theme=(?I5)]')
i6b = FeatStruct('["approval"]')

fs2b_plugged = fs2b.substitute_bindings({Variable('?I0'): i1b, Variable('?I5'): i6b})
fsneub = fs1b.substitute_bindings({Variable('?I2'): i1b, Variable('?I3'): fs2b_plugged})

print(reformat_featstruct(fsneub))

"""
