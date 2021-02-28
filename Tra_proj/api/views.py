from django.shortcuts import render
from api.models import uploadfile, graphfile,graphdata, fileinfo
from api.serializers import uploadfileSerializer, graphfileSerializer,graphdataSerializer,fileinfoSerializer
from api import serializers
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse
from subprocess import Popen, PIPE
from shutil import copyfile
import os
import json
import shutil
from django.utils import timezone
import time
# Create your views here.
from botnet_detection.botdet.data.dataset_botnet import BotnetDataset
from botnet_detection.botdet.eval.evaluation import eval_predictor
from botnet_detection.botdet.eval.evaluation import PygModelPredictor
from torch_geometric.data import Data
import pickle
import csv
import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from Tools.util import *
import traceback
import networkx
import pyvis
from pandas.core.frame import DataFrame

import networkx as nx 
import matplotlib.pyplot as plt


#Create an add, delete, modify and query operation about the user
class uploadfileViewSet(viewsets.ModelViewSet):
    queryset = uploadfile.objects.all()
    serializer_class = uploadfileSerializer

class graphfileViewSet(viewsets.ModelViewSet):
    queryset = graphfile.objects.all()
    serializer_class = graphfileSerializer


class fileinfoViewSet(viewsets.ModelViewSet):
    queryset = fileinfo.objects.all()
    serializer_class = fileinfoSerializer


class getjsonfileAPIView(APIView):
    def get(self, request, format=None):
        get_data = request.query_params.dict()
        result_id = get_data['ID']
        instance = graphdata.objects.get(ID=result_id)
        return Response( json.loads(instance.graphdata) ) 





class getresultAPIView(APIView):

    #Overwrite get method
    def get(self, request, format=None):
        try:    
            get_data = request.query_params.dict()
            result_id = get_data['ID']

            instance = uploadfile.objects.get(ID=result_id)
            uploadData = instance.uploadlocation
            uploadfile_name = "./"+ str(uploadData)

            file_open=open('./botnet_detection/model_cpu.pl','rb')
            model=pickle.load(file_open)
            file_open.close()
            predictor = PygModelPredictor(model)  
            edge_index0=[]
            edge_index1=[]
            edge_y=[]
            y_dic = {}
            with open(uploadfile_name,'r') as csvfile:
                reader = csv.reader(csvfile)
                rows= []
                for index, row in enumerate(reader) :
                    edge_index0.append(int(row[0]))
                    edge_index1.append(int(row[1]))
                    edge_y.append(int(row[2]))
                    y_dic[int(row[0])]=0
                    if int(row[2])==1:
                        y_dic[int(row[0])]=1
                    
            y = []
            for i in y_dic:
                y.append(y_dic[i])
            sub_ts = torch.tensor(np.ones(len(y)),dtype=torch.float32)
            temp_x = sub_ts.reshape(len(y),1)
            temp_edge_index = torch.tensor([edge_index0,edge_index1])
            temp_edge_y = torch.tensor(edge_y,dtype=torch.uint8)
            temp_y = torch.tensor(y, dtype=torch.uint8)
            data_0 = Data(edge_index=temp_edge_index, edge_y=temp_edge_y, x=temp_x, y=temp_y)        
            pred_prob, loss = predictor(data_0)
            result_dict = eval_metrics(data_0['y'], pred_prob)
            pred_cpu = pred_prob.cpu().numpy()
            label= []
            for i in pred_cpu:
                if i >0.5:
                    label.append(1)
                else:
                    label.append(0)  
            pre_edge_y = []
            for i in edge_index0:
                pre_edge_y.append(label[i])

            last = False
            max_number = 0
            last_number = 0
            ind = 0
            for index, i in enumerate(pre_edge_y):
                if i==1:
                    if last:
                        last_number+=1
                    else:
                        last_number=1
                    last = True
                else:
                    last = False
                    last_number=0
                if max_number < last_number:
                    max_number = last_number
                    ind = index

            graph_data = []
            label_dic = {}
            for index, i in  enumerate(edge_index0) :
                label_dic[(i,edge_index1[index])] = pre_edge_y[index]
                label_dic[(edge_index1[index],i)] = pre_edge_y[index]
                graph_data.append((i,edge_index1[index]))
            G=nx.Graph(graph_data)

            def get_2adj(g, node):
                edge_list0 = np.full(len(g.adj[node]),node).tolist()
                edge_list1 = list(g.adj[node])
                for index, i in enumerate(list(G.adj[node])):
                    if index==0:
                        continue
                    edge_list0=edge_list0 + np.full(len(g.adj[i]),i).tolist()
                    edge_list1= edge_list1+ list(g.adj[i])
                    
                return edge_list0,edge_list1

            edge_list0,edge_list1 = get_2adj(G, edge_index0[ind])
            
            if len(edge_list0)<10:
                edge_list0 = edge_index0
                edge_list1 = edge_index1


            edge_y_label = []
            for index,i in enumerate(edge_list0):
                edge_y_label.append(label_dic[(i,edge_list1[index])])

            temp_edge_index0 = edge_list0[:10000]
            temp_edge_index1 = edge_list1[:10000]
            temp_edge_y_label = edge_y_label[:10000]


            new_dic = {}
            index_number = 0
            for i in temp_edge_index0:
                if i not in new_dic.keys():
                    new_dic[i]=index_number
                    index_number+=1
            for i in temp_edge_index1:
                if i not in new_dic.keys():
                    new_dic[i]=index_number
                    index_number+=1

            new_edge_index0=[]
            new_edge_index1=[]
            new_edge_y=[]
            new_edge_y=temp_edge_y_label.copy()
            for i in temp_edge_index0:
                new_edge_index0.append(new_dic[i])
            for i in temp_edge_index1:
                new_edge_index1.append(new_dic[i])
            label_y1_list=[]
            for index, i in enumerate(temp_edge_y_label):
                if i==1:
                    label_y1_list.append(temp_edge_index0[index])

            set_label_y1_list = set(label_y1_list)
            new_label_y=[]
            for i in new_dic.keys():
                if i  in set_label_y1_list:
                    new_label_y.append(1)
                else:
                    new_label_y.append(0)
            add_node = new_edge_index0[-1]+1
            index_number = len(new_dic)

            while add_node < index_number:
                new_edge_index0.append(add_node)
                new_edge_index1.append(add_node)
                new_edge_y.append(0)
                add_node+=1      

            point_size=[10,20]
            color=['#09080d','#cc0202']
            edge_color=['gray','red']
            nodes=[]
            for i in range(new_edge_index0[-1]):
                sub_nodes={}
                sub_nodes['id']=str(i)
                sub_nodes['color']=color[new_label_y[i]]
                sub_nodes['label']=str(i)
                sub_nodes['x']=0
                sub_nodes['y']=0
                sub_nodes['attributes']={}
                sub_nodes['size']=point_size[new_label_y[i]]
                nodes.append(sub_nodes)
                
            links=[]
            for index, i in enumerate(new_edge_index0) :
                sub_links={}
                sub_links['sourceID']=str(i)
                sub_links['targetID']=str(new_edge_index1[index])
                sub_nodes['attributes']={}
                sub_links['size']=point_size[new_edge_y[index]]
                sub_links['color']=edge_color[new_edge_y[index]]
                links.append(sub_links)
                
            json_data = {}
            json_data['nodes']=nodes
            json_data['edges']=links
            split_name = str(uploadData).split('/')[1].split('.csv')[0]

            graphdata_save={
                'graphdata':json.dumps(json_data),
                'graphname':split_name
            }
            serializer = graphdataSerializer(data=graphdata_save)
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save()
            else:
                 return Response({'msg':'graph gen error'})

            point_size=[10,10]
            color=['#09080d','#09080d']
            edge_color=['gray','gray']

            nodes=[]
            for i in range(new_edge_index0[-1]):
                sub_nodes={}
                sub_nodes['id']=str(i)
                sub_nodes['color']=color[new_label_y[i]]
                sub_nodes['label']=str(i)
                sub_nodes['x']=0
                sub_nodes['y']=0
                sub_nodes['attributes']={}
                sub_nodes['size']=point_size[new_label_y[i]]
                nodes.append(sub_nodes)
                
            links=[]
            for index, i in enumerate(new_edge_index0) :
                sub_links={}
                sub_links['sourceID']=str(i)
                sub_links['targetID']=str(new_edge_index1[index])
                sub_nodes['attributes']={}
                sub_links['size']=point_size[new_edge_y[index]]
                sub_links['color']=edge_color[new_edge_y[index]]
                links.append(sub_links)
                
            json_data = {}
            json_data['nodes']=nodes
            json_data['edges']=links
            split_name = str(uploadData).split('/')[1].split('.csv')[0]

            graphdata_save={
                'graphdata':json.dumps(json_data),
                'graphname':split_name
            }
            serializer1 = graphdataSerializer(data=graphdata_save)
            if serializer1.is_valid(raise_exception=True):
                comment1 = serializer1.save()
            else:
                 return Response({'msg':'graph gen error'})






        except Exception as e:
            return Response({'msg': traceback.format_exc()})  

        

        return Response({'result_dict':result_dict,'label_graphid':comment.ID,'unlabel_graphid':comment1.ID}) 




#Upload and analyze files
class uploadfile2APIView(APIView):
    queryset = uploadfile.objects.all()
    serializer_class = uploadfileSerializer

    #Overwrite get method
    # def get(self, request, format=None):
    #     get_data = request.query_params.dict()
    #     result_id = get_data['ID']
    #     result_detail = graphfile.objects.get(ID=result_id)
    #     file_path = result_detail.graphlocation
    #     filename = result_detail.graphname
    #     FilePointer = open(file_path,"rb")
    #     response = HttpResponse(FilePointer,content_type='application/octet-stream')
    #     response['Content-Disposition'] = 'attachment; filename='+filename+'.html'

    #     return response


    #Overwrite post method
    def post(self, request, format=None):
        data = request.data
        fileinfo={}
        serializer1 = uploadfileSerializer(data=data)
        if serializer1.is_valid(raise_exception=True):
            comment1 = serializer1.save()
            uploadData = comment1.uploadlocation
            uploadfile_name = "./"+ str(uploadData)
            label=[]
            sour_ip=[]
            dest_ip=[]  
            anomalous_nodes={} 
            anomalous_edges=0         
            with open(uploadfile_name,'r') as csvfile:
                reader = csv.reader(csvfile)
                rows= []
                for index, row in enumerate(reader) :
                    sour_ip.append(int(row[0]))
                    dest_ip.append(int(row[1]))
                    label.append(0)
                    if int(row[2]) == 1:
                        anomalous_edges+=1
                        anomalous_nodes[int(row[0])]=1


            fileinfo['node_numbers'] = str(sour_ip[-1])
            fileinfo['edges_numbers'] = len(sour_ip)- sour_ip[-1]
            fileinfo['anomalous_ndoes'] = len(anomalous_nodes)
            fileinfo['anomalous_edges'] = anomalous_edges


            temp_edge_index0 = sour_ip[:10000]
            temp_edge_index1 = dest_ip[:10000]
            temp_edge_y_label = label[:10000]


            new_dic = {}
            index_number = 0
            for i in temp_edge_index0:
                if i not in new_dic.keys():
                    new_dic[i]=index_number
                    index_number+=1
            for i in temp_edge_index1:
                if i not in new_dic.keys():
                    new_dic[i]=index_number
                    index_number+=1

            new_edge_index0=[]
            new_edge_index1=[]
            new_edge_y=[]
            new_edge_y=temp_edge_y_label.copy()
            for i in temp_edge_index0:
                new_edge_index0.append(new_dic[i])
            for i in temp_edge_index1:
                new_edge_index1.append(new_dic[i])
            label_y1_list=[]
            for index, i in enumerate(temp_edge_y_label):
                if i==1:
                    label_y1_list.append(temp_edge_index0[index])

            set_label_y1_list = set(label_y1_list)
            new_label_y=[]
            for i in new_dic.keys():
                if i  in set_label_y1_list:
                    new_label_y.append(1)
                else:
                    new_label_y.append(0)
            add_node = new_edge_index0[-1]+1
            index_number = len(new_dic)

            while add_node < index_number:
                new_edge_index0.append(add_node)
                new_edge_index1.append(add_node)
                new_edge_y.append(0)
                add_node+=1      

            point_size=[10,20]
            color=['#09080d','#cc0202']
            edge_color=['gray','red']
            nodes=[]
            for i in range(new_edge_index0[-1]):
                sub_nodes={}
                sub_nodes['id']=str(i)
                sub_nodes['color']=color[new_label_y[i]]
                sub_nodes['label']=str(i)
                sub_nodes['x']=0
                sub_nodes['y']=0
                sub_nodes['attributes']={}
                sub_nodes['size']=point_size[new_label_y[i]]
                nodes.append(sub_nodes)
                
            links=[]
            for index, i in enumerate(new_edge_index0) :
                sub_links={}
                sub_links['sourceID']=str(i)
                sub_links['targetID']=str(new_edge_index1[index])
                sub_nodes['attributes']={}
                sub_links['size']=point_size[new_edge_y[index]]
                sub_links['color']=edge_color[new_edge_y[index]]
                links.append(sub_links)
                
            json_data = {}
            json_data['nodes']=nodes
            json_data['edges']=links
            split_name = str(uploadData).split('/')[1].split('.csv')[0]

            graphdata_save={
                'graphdata':json.dumps(json_data),
                'graphname':split_name
            }
            serializer = graphdataSerializer(data=graphdata_save)
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save()
            else:
                 return Response({'msg':'graph gen error'})

            serializer2 = fileinfoSerializer(data=fileinfo)     
            if serializer2.is_valid(raise_exception=True):
                comment2 = serializer2.save()
            else:
                 return Response({'msg':'fileinfo save error'})


            return Response({'msg':serializer1.data,'graphid':comment.ID,'fileinfoid':comment2.ID})
        else:
            return Response(serializer1.error)


    #Delete files while deleting data records
    def delete(self, request,  format=None):
        try:
            data = request.data
            instance = uploadfile.objects.get(ID=data.get('ID'))
            instance.uploadlocation.delete(save=False)
            instance.delete()

        except Exception as e:
            return Response({'msg': traceback.format_exc()})   
        return Response({'msg':'success'}) 













#Upload and analyze files
class uploadfileAPIView(APIView):
    queryset = uploadfile.objects.all()
    serializer_class = uploadfileSerializer

    #Overwrite get method
    def get(self, request, format=None):
        get_data = request.query_params.dict()
        result_id = get_data['ID']
        result_detail = graphfile.objects.get(ID=result_id)
        file_path = result_detail.graphlocation
        filename = result_detail.graphname
        FilePointer = open(file_path,"rb")
        response = HttpResponse(FilePointer,content_type='text/html')
        response['Content-Disposition'] = 'filename='+filename+'.html'

        return response


    #Overwrite post method
    def post(self, request, format=None):
        data = request.data
        fileinfo = {}
        serializer1 = uploadfileSerializer(data=data)
        if serializer1.is_valid(raise_exception=True):
            comment1 = serializer1.save()
            uploadData = comment1.uploadlocation
            uploadfile_name = "./"+ str(uploadData)
            label=[]
            sour_ip=[]
            dest_ip=[]   
            anomalous_edges = 0  
            anomalous_nodes = {}       
            with open(uploadfile_name,'r') as csvfile:
                reader = csv.reader(csvfile)
                rows= []
                for index, row in enumerate(reader) :
                    sour_ip.append(int(row[0]))
                    dest_ip.append(int(row[1]))
                    label.append(0)
                    if int(row[2])==1:
                        anomalous_edges+=1
                        anomalous_nodes[int(row[0])] = 1

            c = {"source":sour_ip,"destin":dest_ip}


            fileinfo['node_numbers'] = str(sour_ip[-1])
            fileinfo['edges_numbers'] = len(sour_ip)- sour_ip[-1]
            fileinfo['anomalous_ndoes'] = len(anomalous_nodes)
            fileinfo['anomalous_edges'] = anomalous_edges


            df = DataFrame(c)
            if len(df)>2000:
                df = df.sample(n = 2000)
            colorD = {1:"red",0:"black"}
            pic = pyvis.network.Network(height="100%",width="100%",directed=True,notebook=False,bgcolor="white", font_color="black", heading="UnLabeled topology map")
            iplist = []
            for i in range(len(df)):
                sip = df['source'].iloc[i]
                dip = df['destin'].iloc[i]
                ses =str(sip)
                se = int(sip)
                des = str(dip)
                if sip not in iplist:
                  pic.add_node(ses,size=5,color=colorD[0])
                  iplist.append(sip)
                if dip not in iplist:
                    iplist.append(dip)
                    de = int(dip)
                    des = str(dip)
                    pic.add_node(des,size=5,color=colorD[0])
                pic.add_edge(des,ses,physics=True,title=None,width="2px",color=colorD[0])
            split_name = str(uploadData).split('/')[1].split('.csv')[0]
            graphlocation= "./graph/"+split_name+"_graph.html"
            pic.save_graph(graphlocation)

            graphdata={
                'graphlocation':graphlocation,
                'graphname':split_name
            }
            serializer = graphfileSerializer(data=graphdata)
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save()
            else:
                 return Response({'msg':'graph gen error'})


            serializer2 = fileinfoSerializer(data=fileinfo)     
            if serializer2.is_valid(raise_exception=True):
                comment2 = serializer2.save()
            else:
                 return Response({'msg':'fileinfo save error'})


            return Response({'msg':serializer1.data,'graphid':comment.ID,'fileinfoid':comment2.ID})
        else:
            return Response(serializer1.error)


    #Delete files while deleting data records
    def delete(self, request,  format=None):
        try:
            data = request.data
            instance = uploadfile.objects.get(ID=data.get('ID'))
            instance.uploadlocation.delete(save=False)
            instance.delete()

        except Exception as e:
            return Response({'msg': traceback.format_exc()})   
        return Response({'msg':'success'}) 



#Upload and analyze files
class scanfileAPIView(APIView):

    #Overwrite post method
    def post(self, request, format=None):
        try:    
            data = request.data
            instance = uploadfile.objects.get(ID=data.get('ID'))
            uploadData = instance.uploadlocation
            uploadfile_name = "./"+ str(uploadData)

            file_open=open('./botnet_detection/model_cpu.pl','rb')
            model=pickle.load(file_open)
            file_open.close()
            predictor = PygModelPredictor(model)  
            edge_index0=[]
            edge_index1=[]
            edge_y=[]
            y_dic = {}
            with open(uploadfile_name,'r') as csvfile:
                reader = csv.reader(csvfile)
                rows= []
                for index, row in enumerate(reader) :
                    edge_index0.append(int(row[0]))
                    edge_index1.append(int(row[1]))
                    edge_y.append(int(row[2]))
                    y_dic[int(row[0])]=0
                    if int(row[2])==1:
                        y_dic[int(row[0])]=1
                    
            y = []
            for i in y_dic:
                y.append(y_dic[i])
            sub_ts = torch.tensor(np.ones(len(y)),dtype=torch.float32)
            temp_x = sub_ts.reshape(len(y),1)
            temp_edge_index = torch.tensor([edge_index0,edge_index1])
            temp_edge_y = torch.tensor(edge_y,dtype=torch.uint8)
            temp_y = torch.tensor(y, dtype=torch.uint8)
            data_0 = Data(edge_index=temp_edge_index, edge_y=temp_edge_y, x=temp_x, y=temp_y)        
            pred_prob, loss = predictor(data_0)
            result_dict = eval_metrics(data_0['y'], pred_prob)
            pred_cpu = pred_prob.cpu().numpy()
            label= []
            for i in pred_cpu:
                if i >0.5:
                    label.append(1)
                else:
                    label.append(0)  
            pre_edge_y = []
            for i in edge_index0:
                pre_edge_y.append(label[i])

            last = False
            max_number = 0
            last_number = 0
            ind = 0
            for index, i in enumerate(pre_edge_y):
                if i==1:
                    if last:
                        last_number+=1
                    else:
                        last_number=1
                    last = True
                else:
                    last = False
                    last_number=0
                if max_number < last_number:
                    max_number = last_number
                    ind = index

            graph_data = []
            label_dic = {}
            for index, i in  enumerate(edge_index0) :
                label_dic[(i,edge_index1[index])] = pre_edge_y[index]
                label_dic[(edge_index1[index],i)] = pre_edge_y[index]

                graph_data.append((i,edge_index1[index]))
            G=nx.Graph(graph_data)

            def get_2adj(g, node):
                edge_list0 = np.full(len(g.adj[node]),node).tolist()
                edge_list1 = list(g.adj[node])
                for index, i in enumerate(list(G.adj[node])):
                    if index==0:
                        continue
                    edge_list0=edge_list0 + np.full(len(g.adj[i]),i).tolist()
                    edge_list1= edge_list1+ list(g.adj[i])
                    
                return edge_list0,edge_list1

            edge_list0,edge_list1 = get_2adj(G, edge_index0[ind])


            new_dic = {}
            index_number = 0
            for i in edge_list0:
                if i not in new_dic.keys():
                    new_dic[i]=index_number
                    index_number+=1
            for i in edge_list1:
                if i not in new_dic.keys():
                    new_dic[i]=index_number
                    index_number+=1


            new_edge_index0=[]
            new_edge_index1=[]
            new_edge_y=[]
            new_edge_y=pre_edge_y.copy()
            for i in edge_list0:
                new_edge_index0.append(new_dic[i])
            for i in edge_list1:
                new_edge_index1.append(new_dic[i])


            edge_y_label = []
            label_y1_list=[]
            for index,i in enumerate(edge_list0) :
                try:
                    edge_y_label.append(label_dic[(i,edge_list1[index])])
                    if label_dic[(i,edge_list1[index])]== 1 :
                        label_y1_list.append(i)
                    
                except:
                    pass
            set_label_y1_list = set(label_y1_list)
            
            new_label_y=[]
            for i in new_dic.keys():
                if i  in set_label_y1_list:
                    new_label_y.append(1)
                else:
                    new_label_y.append(0)                    



            label= new_label_y        
            sour_ip=new_edge_index0
            dest_ip=new_edge_index1

            c = {"source":sour_ip,"destin":dest_ip}
            df = DataFrame(c)
            if len(df)>2000:
                df = df.sample(n = 2000)
            colorD = {1:"red",0:"black"}
            pic = pyvis.network.Network(height="100%",width="100%",directed=True,notebook=False,bgcolor="white", font_color="black", heading="Labeled topology map")
            pic1 = pyvis.network.Network(height="100%",width="100%",directed=True,notebook=False,bgcolor="white", font_color="black",heading="UnLabeled topology map")
            iplist = []
            for i in range(len(df)):
                sip = df['source'].iloc[i]
                dip = df['destin'].iloc[i]
                ses =str(sip)
                se = int(sip)
                des = str(dip)
                if sip not in iplist:
                  pic.add_node(ses,size=5,color=colorD[label[se]])
                  pic1.add_node(ses,size=5,color=colorD[0])
                  iplist.append(sip)
                if dip not in iplist:
                    iplist.append(dip)
                    de = int(dip)
                    des = str(dip)
                    pic.add_node(des,size=5,color=colorD[label[de]])
                    pic1.add_node(des,size=5,color=colorD[0])
                pic.add_edge(des,ses,physics=True,title=None,width="2px",color=colorD[label[se]])
                pic1.add_edge(des,ses,physics=True,title=None,width="2px",color=colorD[0])
            split_name = str(uploadData).split('/')[1].split('.csv')[0]
            graphlocation= "./graph/"+split_name+"_label_graph.html"
            graphlocation1= "./graph/"+split_name+"_label_graph1.html"
            pic.save_graph(graphlocation)
            pic1.save_graph(graphlocation1)




            graphdata={
                'graphlocation':graphlocation,
                'graphname':split_name
            }


            serializer = graphfileSerializer(data=graphdata)
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save()
            else:
                 return Response({'msg':'graph gen error'})


            graphdata1={
                'graphlocation':graphlocation1,
                'graphname':split_name
            }


            serializer1 = graphfileSerializer(data=graphdata1)
            if serializer1.is_valid(raise_exception=True):
                comment1 = serializer1.save()
            else:
                 return Response({'msg':'graph gen error'})



        except Exception as e:
            return Response({'msg': traceback.format_exc()})  


        return Response({'result_dict':result_dict,'label_graphid':comment.ID, 'unlabel_graphid':comment1.ID}) 

