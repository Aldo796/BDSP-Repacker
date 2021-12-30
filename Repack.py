import os, rapidjson, UnityPy, glob, traceback, time

from PIL import Image

def repackassets(src, output):
    ##Creates a new folder named {src}_Export
    ##Puts files from source in folder
    extract_dir = str(src) + "_Export"
    path_dir = "pathIDs"
        
    filename = os.path.basename(src)   
    fp = os.path.join(path_dir, f"{filename}_pathIDs.json")
    with open(fp, "r") as f:
        pathDic = rapidjson.load(f)
        pathDicKeys = list(pathDic.keys())
    if os.path.exists(extract_dir):
        try:
            env = UnityPy.load(src)
            for obj in env.objects:
                if obj.type.name == "MonoBehaviour":
                    # export
                    if obj.serialized_type.nodes:
                        # save decoded data
                        if str(obj.path_id) in pathDicKeys:
                            
                            name = pathDic[str(obj.path_id)]
                        
                        else:
                            
                            tree = obj.read_typetree()
                            
                            name = tree["m_Name"]
                            
                            if name == "":
                                script_path_id = tree["m_Script"]["m_PathID"]
                                for script in env.objects:
                                    if script.path_id == script_path_id:
                                        name = script.read().name
                                    
                        fp = os.path.join(extract_dir, f"{name}.json")
                        with open(fp, "r", encoding = "utf8") as f:
                            obj.save_typetree(rapidjson.load(f))
                    else:
                        # save raw relevant data (without Unity MonoBehaviour header)
                        data = obj.read()
                        fp = os.path.join(extract_dir, f"{data.name}.bin")
                        with open(fp, "rb") as f:
                            obj.set_raw_data(f.read())
            
            fp = os.path.join(output, os.path.basename(src))
            with open(fp, "wb") as f:
                f.write(env.file.save(packer=(64,2))) 
                f.close()               
            return(f"{src} repacked successfully")
        
        except:
            
            print(traceback.format_exc())
            return(f"{src} failed to repack")
    else:
        
        print("Error: "f"{src}_Export does not exist (Have you ran Unpack.exe?)")
    

start_time = time.time()
path = "AssetFolder"
output = "EditedAssets"

if not os.path.exists(path):
    os.makedirs(path, 0o666)
    print("Created folder 'AssetFolder' put Unity Assets e.g. masterdatas, ev_scripts in folder")
    input("Once all files are in, press enter to continue...")
    
if not os.path.exists(output):
    os.makedirs(output, 0o666)

i = 0
for filepath in glob.iglob(path + "**/**", recursive=False):
    if os.path.isfile(filepath):
        i += 1
        print(repackassets(filepath, output))
        
print("Finished Repacking "f"{i} Files")
print("Repacking took", time.time() - start_time, "seconds to run")
input("Press Enter to Exit...")