python3.x

# traffic-classification
conda install pytorch==1.4.0 torchvision==0.5.0 cudatoolkit=10.1 -c pytorch
</br>
python -m pip install pip==19.3</br>
pip install torch-scatter==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-sparse==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-cluster==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-spline-conv==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-geometric==1.4.3</br>
pip install pyvis</br>  

# if no GPU

python -m pip install pip==19.3</br>
pip install torch-scatter==2.0.3+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-sparse==0.6.1+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-cluster==1.5.3+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-spline-conv==1.2.0+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html</br>
pip install torch-geometric==1.4.3</br>



# in Tra_proj/botnet_detection/  start back end
pip install deepdish </br>
python setup.py install</br>
pip install django</br>
pip install djangorestframework</br>
pip install django-cors-headers</br>


python manage.py makemigrations</br>
python manage.py migrate</br>


python manage.py runserver 0.0.0.0:8788</br>


# in  Tra_proj/basic/ start front End
First of all, you need to modify the front-end interface to access ip according to the backend ip.
in Tra_proj/basic/src/service/index.ts  BASE_URL Change it to the ip address where the backend is located. Use localhost:8788 if running locally

in Tra_proj/basic/public/    labeledgraph.html and  unabledgraph.html Change the ip part of var base to backend ip.


Nodejs should be installed on your device.

install yarn first:

> npm install -g yarn

then enter the entry:

> yarn

after all of the deps are ready, run it:

> yarn run start

open your browser and goto `localhost:3000` to visit it!

