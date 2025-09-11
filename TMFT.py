import re
from collections import defaultdict
import os,glob

excluded = {
    'out'
}

colors = {
    'red','orange','yellow','green','cyan','teal','blue','purple','violet','grey','gray','silver','black','brown','white'
}

synonym_dict = {
    "footwear": "boots",
    "shoes": "boots",
    "eye gear": "glasses",
    "head gear": "hat",
    "swimming suit": "swimsuit",
    "eyewear": "glasses",
    "headwear": "hat" ,
    'fangs':'fang',
    'stomach':'navel',
    'midriff':'navel',
    'bandages':'bandaged',
    'frills':'frilled',
    'blonde':'white', 
    'dog':'wolf',
    'ear':'ears'
}
blacklist = 'looking at viewer,multiple girls,skeb commission,textless version,conversion,gif,bad id,bad pixiv id,absurdres,commentary request,translation request,translated,borrowed character,kemono friends'.split(',')
    
def ears(tags):
    specific = len([t for t in tags if ' ears' in t and 'animal ears' != t])>0
    if specific:
        tags = [t for t in tags if t != 'animal ears']
        print('- animal ears')
    return tags
    
def apply_synonym_replacement(tag, allTags):
    sorted_keys = synonym_dict.keys()#sorted(synonym_dict.keys(), key=lambda x: len(x), reverse=True)
    tag2=tag
    for key in sorted_keys: 
        if synonym_dict[key] in ','.join(allTags) and '(' not in tag:
            pattern = r'(^|\s)' + re.escape(key) + r'($|\s)'
            replacement = r'\1' + synonym_dict[key] + r'\2'
            tag2 = re.sub(pattern, replacement, tag)
            #tag2 = tag.replace(key,synonym_dict[key])
            if tag2 != tag:
                print(key,'->',synonym_dict[key]) 
                print(tag,'->',tag2) 
                return tag2   
    return tag2

    
def remove_blacklisted(tags):
    return [re.sub(r'(\(.+\))\s.+',r'\1',tag) for tag in tags if tag not in blacklist]
        
        
def subsume(tags):
    tags = list(set(tags)) 
    
    kept_tags = []
    for tag in tags: 
        found = False
        found = any([(t.endswith(tag) or t.startswith(tag)) and t != tag for t in tags])
        if not found:
            kept_tags.append(tag)
        elif tag != '':
            print('-',tag)
    result = kept_tags
    return result
    
def merge(tags):
    tags = list(set(tags)) 
    tree = defaultdict(list)
    joined = ','.join(tags)
    for tag in tags:
        if '(' in tag:
            pass
        else:
            words = tag.split(' ')
            if len(words) == 2 and words[-1] not in excluded:
                for t in tags:
                    if t!= tag and t.endswith(words[-1]) and len(t.split(' ')) == 2:
                        tree[words[-1]].append(words[0])
    for noun in tree.keys():
        if 'multicolored' in tree[noun] and noun == 'hair':
            tree[noun] = [adj for adj in tree[noun] if adj not in colors]
            
        for adj in tree[noun]:
            try:                
                tags.remove(adj+' '+noun)
                print('-',adj+' '+noun)
            except Exception as e:
                pass
        merged = list(set(tree[noun]))         
        print('+',' '.join(merged)+' '+noun)
        tags.append(' '.join(merged)+' '+noun)
    return tags
    
def clrs(tags):
    remved = []
    if re.compile(r'multicolored.+hair').search(','.join(tags)):
        for clr in colors:
            for t in tags:
                if re.search(clr+' hair',t) and not 'multicolored' in t:
                    remved.append(t)
        print('-',remved)
    return [t for t in tags if t not in remved]
    
def x_girl(tags):
    r = re.compile("^(\w{3,})\sgirl$")
    hasXgirl = [x for x in tags if r.match(x)]
    if len(hasXgirl)>0:
        x = hasXgirl[0].replace(' girl','')
        r = re.compile(r"^"+x+"\s\w+$")
        removed = [t for t in tags if r.match(t) and t != x + ' girl']
        print('-',removed)
        tags = [t for t in tags if t not in removed]
    return tags      
        

# Example usage
if __name__ == "__main__":
    input_tags=[]
    search_pattern = os.path.join("C:\\Users\\paran\\Downloads\\tanaka\\unsafe\\", "*.txt")
    for file_path in glob.glob(search_pattern):
        print(f"Processing file: {file_path}")
        with open(file_path, "r") as f:
         input_tags = f.read().split(', ')

        #print('Had:',input_tags, round(len(','.join(input_tags))/3.33),'tokens')
        lb4=len(','.join(input_tags))
        total = clrs(merge(x_girl(subsume(ears([apply_synonym_replacement(tag,input_tags) for tag in remove_blacklisted(input_tags)])))))
        #print('Got:',', '.join(sorted(total)))
        #print(lb4,len(','.join(total)))
        print('Saved ~',round((lb4-len(','.join(total)))/3.33), 'tokens')
        with open(file_path, "w") as f:
         f.write(', '.join(total))