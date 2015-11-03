#General principles

Git is a popular version control software that can do a TON of cool stuff. However, for our purposes, git is just going to be used to save versions of software and perhaps collaborate on projects with each other. GitHub is a cloud-based version of git; it allows you to backup, update, access, and share your projects online. Key terms are:
1. *Repositiories (repos)* are essentially folders which contain entire projects
2. *Branches* are 'different versions' on the same project: if your project pipeline uses multiple scripts and you want to make changes to many files without potentially 'breaking' the current version of the pipeline, you can create a new branch, edit your files, and once everything is working and tested, merge the original branch and the new branch. The 'master' branch is where you should store the latest WORKING version of your project, and you can create other branches to experiment on
3. *Commiting* is something you will learn to love. Typically the workflow goes as follows: you are working on your local machine, make a few changes to your code, and you COMMIT. Commiting saves the current 'version' of your file. You don't want to commit after every small change, but you also don't want to wait too long to commit! A
4. *Pushing* is when you sync files from your local machine to github. After several commits (generally when you have made a substantial change to the code) you push these commits to github, which backs up your versions on the cloud. You can then 'roll back' to a previous commit whenever you want!

# Configuring Github for the first time
**Set up accounts** 
* First thing first, set up your local git profile (on your machine)

```bash
git config --global user.name "Bill Murray"
git config --global user.email "BM_ghostbuster@talent.com"
```
* If you haven't already done so, create an account on github.com (preferably with the same info as before)

**Prepare local directory**
* It's a good idea to create a new directory to house all of your git repositiories.

```bash
mkdir ~/Documents/git_repos
```

This is where you will store all of your repositories in the future. For example, a project called 'black_box' would be in ```~/Documents/git_repos/black_box```

**Copying files**
* If you already have repos on github.com that you wish to copy to your local machine, you can do so with the following command:
```bash
git clone https://github.com/<username>/<repository>
```
* Alternatively, if you have files on your local machine which you wish to upload to Github.com, you should first copy (or move) the files from their current location into your new git_repos dir- using the dir 'black_box' as an example:
```bash
cp -r ~/Documents/old_project_folder/black_box  ~/Documents/git_repos/
git init ~/Documents/git_repos/black_box
```

**Setting up SSH connection**
If you don't mind entering your username and password every time you want to push changes to github, you can skip this section. If that is the case, you probably need to have a stronger password, or you need to push updates more often!

* Generate a RSA key using the following commands. This will allow you to push your commits to github without having to authenticate every time:
```bash
ssh-keygen -t rsa -b 4096 -C "BM_ghostbuster@talent.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
 ```
 * Copy the contents of .ssh/id_rsa.pub (it should start with 'ssh-rsa') and add a new SSH key at https://github.com/settings/ssh
 
#Using git with github
 **Commiting**
 * Now that you have a repository on your local machine, you can start making changes
 
 1064  git commit fasta-to-gtf.py -m "testing terminal commands"

 1077  git push fasta-to-gtf https://github.com/willblev/fasta-to-gtf/master
 1078  ll
 1079  cd src/
 1080  git commit fasta-to-gtf.py -m "test2"
 1081  git push origin master
 

 1099  git commit fasta-to-gtf.py -m "testi4"

 1103  head id_rsa
 1104  cat id_rsa.pub
 1105  git push origin master
 1106  cd  -

 1109  ll /home/william/.ssh/

 1113  git remote set-url origin git@github.com:/willblev/fasta-to-gtf.git
 1114  git remote -v

