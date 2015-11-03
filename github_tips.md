#General principles

Git is a version manager/

# Configuring Github for the first time
**Set up accounts** 
* First thing first, set up your local git profile (on your machine)

```bash
git config --global user.name "Bill Murray"
git config --global user.email "BM_ghostbuster@talent.com"
```
* If you haven't already done so, create an account on github.com (preferably with the same info as before)

**Prepare local directory**
* It's a good idea to create a separate folder to house your git repositiories; repositiories (repos) are essentially folders for different projects.

```bash
mkdir ~/Documents/git_repos
```

This is where you will store all of your repositories in the future. For example, a project called 'black_box' would be in ```~/Documents/git_repos/black_box```

**Copy files**
* If you already have repos on github.com that you wish to copy to your local machine, you can do so with the following command:
git clone https://github.com/<username>/<repository>
* Alternatively, if you have files on your local machine which you wish to upload to Github.com, you must first copy the files into 
git add

 1064  git commit fasta-to-gtf.py -m "testing terminal commands"

 1077  git push fasta-to-gtf https://github.com/willblev/fasta-to-gtf/master
 1078  ll
 1079  cd src/
 1080  git commit fasta-to-gtf.py -m "test2"
 1081  git push origin master
 1082  ssh-keygen -t rsa -b 4096 -C "willblev@gmail.com"
 1083  eval "$(ssh-agent -s)"
 1084  ssh-add /home/william/.ssh/id_rsa
 1085  cat /home/william/.ssh/id_rsa.pub

 1099  git commit fasta-to-gtf.py -m "testi4"

 1103  head id_rsa
 1104  cat id_rsa.pub
 1105  git push origin master
 1106  cd  -

 1109  ll /home/william/.ssh/

 1113  git remote set-url origin git@github.com:/willblev/fasta-to-gtf.git
 1114  git remote -v

