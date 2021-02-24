# traffic-classification
conda install pytorch==1.4.0 torchvision==0.5.0 cudatoolkit=10.1 -c pytorch

python -m pip install pip==19.3
!pip install torch-scatter==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-sparse==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-cluster==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-spline-conv==latest+cu101 -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-geometric==1.4.3
!pip install pyvis

# in Tra_proj/botnet_detection/
!pip install deepdish 
!python setup.py install
!pip install django
!pip install djangorestframework
!pip install django-cors-headers


python manage.py runserver 0.0.0.0:8788


# if no GPU

python -m pip install pip==19.3
!pip install torch-scatter==2.0.3+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-sparse==0.6.1+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-cluster==1.5.3+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-spline-conv==1.2.0+cpu -f https://pytorch-geometric.com/whl/torch-1.4.0.html
!pip install torch-geometric==1.4.3
