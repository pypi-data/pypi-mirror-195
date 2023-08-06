class LibraCodex:
    
    def __init__(self):
        self.Codex = {}
        
    #add paths to main container.
    def add_paths(self,tag_name,user_path):
        import os
        if not os.path.isdir(user_path):
            raise Exception("Invalid path! please try again!")
        elif not os.path.exists(user_path):
            raise Exception("Invalid path! please try again!")
        else:
            self.Codex[tag_name] = user_path
    
    #update path to main container.
    def update_paths(self,tag_name,new_user_path):
        import os
        
        if not os.path.isdir(new_user_path):
            raise Exception("Invalid path! please try again!")
        elif not os.path.exists(new_user_path) :
            raise Exception("Invalid path! please try again!")
        else:
            print("Complete!")
            self.Codex.update({tag_name:new_user_path})
    
    #select you're path at desire by use tag_name get paths.
    def select_to_codex(self,tag_name):
        return self.Codex.get(tag_name)
    
    #connect all paths in once time.
    def full_to_codex(self):
        return self.Codex.values()
    
    #clear all paths and than return None when after delete finish.
    def washing_paths(self):
        self.Codex.clear()
        return None
    
    #show all paths in container.
    def preview(self):
        for tag , path in self.Codex.items():
            print(f"---{tag}-=-{path}---",sep="\n")
    
#simple convert // to /    
def paths_converter(old_path):
    if isinstance(old_path,str):
        new_path = old_path.replace("\\","/")
        return str(new_path)    
    elif isinstance(old_path,(int,float,complex)):
        raise TypeError("Invalid type! please should using only 'str' datatype.")
    

