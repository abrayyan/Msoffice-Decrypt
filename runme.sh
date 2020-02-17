git clone git@gitlab.com:abrayyan/msoffice_decrypt.git &&
cd msoffice_decrypt &&
docker build -t modecrypt:v1 . &&
cd msoffice_decrypt &&
SET CURRENTDIR=%cd% &&
docker run --rm -it --cpus=2 --mount type=bind,target=/msoffice_decrypt,source=$PWD modecrypt:v1 bash -c "cd /msoffice_decrypt; ls; python3 generate_password_combinations.py"