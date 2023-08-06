class LibraCodex:

    def __init__(self):
       self.Codex = {}
        
    #add paths to main container.
    def add_paths(self,tag_name,user_path):
        import os

        if not os.path.isdir(user_path):
            raise OSError("Invalid path! please try again!")
        elif not os.path.exists(user_path):
            raise OSError("Invalid path! please try again!")
        elif not os.path.abspath(user_path):
            raise OSError("Invalid path! please try again!")
        else:
            self.Codex[tag_name] = user_path
            
    #add only absolute paths. 
    def add_paths_by_absolute(self,tag_name,users_paths):
        import os
        if not os.path.isabs(users_paths):
           raise OSError(f"Invalid path! by {users_paths} aren't absolute path. please try again!")
        else:
            print("Complete!")
            self.Codex[tag_name] = users_paths

    #update path to main container.
    def update_paths(self,tag_name,new_user_path):
        import os
        if not os.path.isdir(new_user_path):
            raise OSError()("Invalid path! please try again!")
        elif not os.path.exists(new_user_path) :
            raise OSError()("Invalid path! please try again!")
        else:
            print("Complete!")
            self.Codex.update({tag_name:new_user_path})

    #select you're path at desire by use tag_name get paths.
    def path_chooser(self,tag_name):
        print(f" You're pick {tag_name} ")
        return self.Codex.get(tag_name)
    
    #clear all paths and than return None when after delete finish.
    def washing_paths(self):
        self.Codex.clear()
        return None
   
    def configure_path(self,reference_tags_1,reference_tags_2):
        
        default_path_1 = self.Codex.get(reference_tags_1)
        print(f'setup a {default_path_1} in default paths ')
        default_path_2 = self.Codex.get(reference_tags_2)
        print(f'setup a {default_path_1} in default paths ')
        
        return default_path_1 , default_path_2
        
    #show all paths in container.
    def preview(self):
        for tag , path in self.Codex.items():
         print(f"---{tag}-=-{path}---",sep="\n")

#simple convert // to / 
def paths_converter(old_path):
    if isinstance(old_path,str):
        new_path_1 = old_path.replace("\\","/")
        return str(new_path_1)
    elif isinstance(old_path,(int,float,complex)):
        raise TypeError("Invalid type! please should using only 'str' datatype.")
    else:
        pass
    

