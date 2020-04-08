# Double Open Yocto Readme

## How to get here

Follow the instructions in [Yocto Project Quick Build](https://www.yoctoproject.org/docs/3.0.2/brief-yoctoprojectqs/brief-yoctoprojectqs.html) for the most parts.

### Use Git to Clone Poky

After cloning poky from https://git.yoctoproject.org/git/poky and checking out tag `yocto-3.0.2` to your new branch, add a new remote for https://git.yoctoproject.org/git/poky-contrib. From branch [rpurdie/license-experiments-osls](https://git.yoctoproject.org/cgit/cgit.cgi/poky-contrib/log/?h=rpurdie/license-experiments-osls) of poky-contrib, apply commits [bf9305ad33791536c3db4fc3e11b5d698d928cd9](https://git.yoctoproject.org/cgit/cgit.cgi/poky-contrib/commit/?h=rpurdie/license-experiments-osls&id=bf9305ad33791536c3db4fc3e11b5d698d928cd9) and [51f58f4caa9d70a7621009d9ea59bbbf5e3928b2](https://git.yoctoproject.org/cgit/cgit.cgi/poky-contrib/commit/?h=rpurdie/license-experiments-osls&id=51f58f4caa9d70a7621009d9ea59bbbf5e3928b2) to your branch. This can be done with `git cherry-pick bf9305ad33791536c3db4fc3e11b5d698d928cd9` and `git cherry-pick 51f58f4caa9d70a7621009d9ea59bbbf5e3928b2`.

After applying the commits, you're ready to proceed with the Quick Build.