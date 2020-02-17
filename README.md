# MSOffice Decrypt Tool

This tool automate decrypting msoffice files by generating different types of permutations and uses brute force to estimate
the possible combinations reporting it if any found. The tool is based on the opensource project [msoffcrypto-tool](link_to_msoffcrypto_tool).


## Installation

the tool is deployed within a docker container to simplify installing the dependencies. Please go throw the steps below in order to build and install the tool.

1. Sign up in github or gitlab.
2. Download git, for windows download using [this source](https://git-scm.com/downloads). 
3. Install git and configure it on your machine, go throw the following steps a - d to configure it other wise skip to step 4.
	a. Open your terminal/(Powershell in windows) and make sure that git is installed by executing `git --version`.
	b. Configure your user name (your git user name) using the command `git config --global user.name YOUR_GIT_USERNAME` ex:. `git config --global user.name myusername`.
	c. Configure your email address you use to sign in git using the command `git config --global user.email YOUR_EMAIL` ex:. `git config --global user.email myemail@gmail.com`.
	d. Generate a public ssh key and add it to your trusted keys in your git account:
		- Type the command `ssh-keygen -t ed25519 -C "YOUR_EMAIL"` ex:. `ssh-keygen -t ed25519 -C "myemail@gmail.com"`.
		- This command should generate 2 keys (public and private) and mostly will put them in the directory '/home/YOURMACHINE/.ssh' or 'C:\Users\YOURMACHINE\.ssh\' under file names id_ed25519 and id_ed25519.pub.
		- Copy the content of id_ed25519.pub which is your public key.
		- Log in to your git account (github or gitlab doesnt matter), got to setting, then ssh keys, then add new key.
		- Paste the key there and assign any name you want for it.
4. Download docker from here and install it on your machine [from here](https://docs.docker.com/docker-for-windows/install/).
5. You are all set now, you just need to execute the batch file 'runme.bat' for windows or the shell file 'runme.sh' included with this file.
	a. Create a new directory on your machine where you would want the tool to be installed.
	b. Place the batch/shell file in that directory.
	c. Open windows powershell or terminal and cd into that directory (redirect the shell to that directory).
	d. Execute the batch file using the shell by typing the command `./runme.bat` or the shell file `bash runme.sh`. (Please check the notes below to understand the commands the batch file is executing)
	
	```
	git clone git@gitlab.com:abrayyan/msoffice_decrypt.git &
	cd msoffice_decrypt &
	docker build -t modecrypt:v1 . &
	cd msoffice_decrypt &
	SET CURRENTDIR=%cd% &
	docker run --rm -it --cpus=2 --mount type=bind,target=/msoffice_decrypt,source=%CURRENTDIR% modecrypt:v1 bash -c "cd /msoffice_decrypt; ls; python3 generate_password_combinations.py"
	```
	
	- `git clone git@gitlab.com:abrayyan/msoffice_decrypt.git`        (Clones my code from my repo, I should give you access to your account before to be able to clone it)
	- `cd msoffice_decrypt`                                           (Redirecting the shell into the msoffice_decrypt directory)
	- `docker build -t modecrypt:v1 .`								  (Builds a new docker container using the Dockerfile included in the repo)
	- `cd msoffice_decrypt`
	- `SET CURRENTDIR=%cd%`
	- `docker run --rm -it --cpus=2 --mount type=bind,target=/msoffice_decrypt,source=%CURRENTDIR% modecrypt:v1 bash -c "cd /msoffice_decrypt; ls; python3 generate_password_combinations.py"`								  (Run the container you have just built and mount the current directory into the root of the container)
	
## Use Details

The script included 'generate_password_combinations.py' is what does most of the work by generating different password combinations if they do not exist on your machine and loop over them to try which one of them
is the password. The main function that can be called with your custom parameters is the one below:
```
decrypt_file(msOfficeFilePath,
             permutationsDirectoryPath,
             psswdLength,
             minPsswd=1,
             withDigits=True,
             withLowerLetters=False,
             withUpperLetters=False,
             withSpecialCharacters=False,
             multiCore=False,
             numberOfCores=None,
             psswdRange=None)
```

- **msOfficeFilePath** : Path to the msoffice file.
- **permutationsDirectoryPath** : The directory where the permutations will be saved.
- **psswdLength** : Maximum length of password to try.
- **minPsswd** , int , default=1 : Minimum length of password to try.
- **withDigits** , bool , default=True : Use if password might contain digits ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
- **withLowerLetters** , bool , default=False : Use if password might contain small letters ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
- **withUpperLetters** , bool , default=False : Use if password might contain capital letters ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
- **withSpecialCharacters** , bool , default=False : Use if password might contain special characters ['!', '@', '#', '$', '%', '^', '&', '*']
- **multiCore** , bool , default=False : Use if you want the tool to use multi cores in parallel to speed up finding the password.
- **numberOfCores** , bool , default=None : Specify how many cores to use, if None this means use all available.
- **psswdRange** , tupple , default=None : Experimental do not use.

	
## Example

* Find password for the file "enccrypted.xlsx" , use permutations at the directory "permutations/" (if no permutations available in that directory in will generate new ones), password might only contain digits, check up to maximum of 5 passwords, use 6 processors to do the processing.
```
pwd = decrypt_file(msOfficeFilePath="enccrypted.xlsx",
                   permutationsDirectoryPath="permutations/",
                   withDigits=True,
                   psswdLength=5,
                   multiCore = True,
                   numberOfCores = 6)
```

