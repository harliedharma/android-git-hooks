# android-git-hooks
Git hooks collection for Android project:
- Pre-commit code autoformat with Intellij formatter in Android Studio
- Todo: Pre-commit Android linter

Requirements
------------
Android Studio is installed and you must set ANDROID_STUDIO environment variable with Android Studio's path.
In MacOS: /Applications/Android Studio.app

How to Use
----------
Add the contents of this repo to your root project
1. `$ cd $PROJECT`
2. `$ git remote add android-git-hooks https://github.com/harlie2120/android-git-hooks.git`
3. `$ git subtree add --prefix=git-hooks/ android-git-hooks master`

Any person who clones your project must symlink the folder into .git folder
1. `$ cd .git && mv hooks hooks.old && ln -s ../git-hooks hooks`

You can update the hooks inside your project
1. `$ git fetch android-git-hooks master`
2. `$ git subtree pull --prefix=git-hooks/ android-git-hooks master`
