import github3




def push_to_git(username,password,path,account,repo,message):
    import github3
    files_to_upload = [path]
    gh = github3.login(username=username, password=password)
    repository = gh.repository(account, repo)
    for file_info in files_to_upload:
        with open(file_info, 'rb') as fd:
            contents = fd.read()
        push_status = repository.create_file(
            path=file_info,
            message=message.format(file_info),
            content=contents,
        )

    return type(push_status)!=github3.null.NullObject



def update_to_git(username,password,path,account,repo,message):
    files_to_upload = [path]
    gh = github3.login(username=username, password=password)
    repository = gh.repository(account, repo)
    for file_info in files_to_upload:
        with open(file_info, 'rb') as fd:
            contents = fd.read()
        contents_object = repository.contents(file_info)
        if contents_object:
            push_status = contents_object.update(message,contents)
            print str(push_status)
        else:
            print "file doesn't exist on repo"


def push_update_to_git(username,password,path,account,repo,message):
    files_to_upload = [path]
    gh = github3.login(username=username, password=password)
    repository = gh.repository(account, repo)
    for file_info in files_to_upload:
        with open(file_info, 'rb') as fd:
            contents = fd.read()
        contents_object = repository.contents(file_info)
        if contents_object:#this file already exists on remote repo
            #update
            push_status = contents_object.update(message,contents)
            print push_status
        else:#file doesn't exist on remote repo
            #push
            push_status = repository.create_file(path=file_info, message=message.format(file_info),content=contents,)
            print push_status['commit']
            
#4ou__-e680_P80OjtrCJD






files_to_upload='uploaded_commits/somethingh.txt'
username='zangsir@gmail.com'
password='zs12084'
account='zangsir'
repo='coptic-xml-tool'
message='try panera'

push_update_to_git(username,password,files_to_upload,account,repo,message)
