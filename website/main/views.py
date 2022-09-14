from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from .models import Student, Question
import random

# import tensorflow as tf
# import tensorflow_hub as hub
# import glob
# import pandas as pd
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.corpus import genesis
# from nltk.corpus import wordnet_ic
# from nltk.corpus import wordnet as wn
# from nltk.stem import PorterStemmer
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import RegexpTokenizer
# import gensim
# from gensim.models import doc2vec
# from collections import namedtuple
# from gensim.models import Word2Vec
# from sklearn.feature_extraction.text import TfidfVectorizer
# import re
# import math
# import numpy as np
# from sklearn.decomposition import TruncatedSVD
# from sklearn.preprocessing import Normalizer
# from sklearn import metrics
# from scipy import spatial
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score


def index(request):
    
    return render(request, 'index.html')

def student_consent(request):
    return render(request, 'student_consent.html')

def assessment(request):
    # Get 3 random questions that have not been answered
    questions = list(Question.objects.filter(is_answered=False))
    questions = random.sample(questions,3)
    context = {'questions':questions}
    return render(request,'assessment.html', context)

def assessment_end(request):
    if request.method == 'POST':
        message = ""
        if 'student' in request.session:
            message = "You have already completed this survey."
        else:
            answers = request.POST.getlist('answers[]')
            student = Student()
            questions = Question.objects.all().filter(student=student)
            for i, j in zip(questions, answers):
                i.stu_answer = j
                i.save()
            student = Student()
            student.save()
            request.session['student'] = student.id
            for question in questions:
                question.is_answered = True
                question.student = student
        context = {'message':message}
        return render(request, 'assessment_end.html', context)


# def marker_index(request):
#     return render(request, 'marker_index.html')

# def marker_consent(request):
#     return render(request, 'marker_consent.html')

# def marking(request):
#     students = list(Question.objects.all())
#     students = random.sample(students,3)
#     questions = Question.objects.all()
#     context = {'students':students, 'questions':questions}
#     for student in students:
#         print(student.id)
#     return render(request, 'marking.html', context)


# tokenizer = RegexpTokenizer(r'\w+') #will remove punctuations
# lemmatizer = WordNetLemmatizer()
# stop_words = set(stopwords.words('english'))
# genesis_ic=wn.ic(genesis, False, 0.0)

# def get_tdata():
#   direc=glob.glob('Semeval Data XMLtocsv/*.csv')
#   direc.sort()
#   df=[]
#   for s in direc:
#     df.append(pd.read_csv(s))
#   ref_ans=[]
#   f = open(r"Semeval Data XMLtocsv/ref_ans.txt", "r")
#   for x in f:
#     if x=='\n':
#       continue
#     ref_ans.append(x.strip())
#   question=[]
#   f = open(r"Semeval Data XMLtocsv/question.txt", "r")
#   for x in f:
#     if x=='\n':
#       continue
#     question.append(x.strip())
#   stud_ans=[]
#   accuracy=[]
#   for i in range(len(df)):
#       stud_ans.append([j for j in df[i]['__text']])
#       accuracy.append([j for j in df[i]['_accuracy']])
#   corr=0
#   incorr=0
#   Y=[]
#   for i in range(0,len(stud_ans)):
#       for j in range(len(accuracy[i])):
#           if(accuracy[i][j]=="correct"):
#               Y.append(1)
#               corr=corr+1
#           else:
#               Y.append(0)
#               incorr=incorr+1
#   print(len(stud_ans),len(ref_ans),len(question),len(Y))
#   return stud_ans,ref_ans,question,Y
# stud_ans,ref_ans,question,Y=get_tdata()

# print(ref_ans[0])

# def get_func_words():
#   file=open(r"function_words")
#   func_words=[]
#   pattern=r"\w+'?\w*"
#   for i in file.readlines():
#     result=re.findall(pattern,i)
#     for j in result:
#         func_words.append(j)
#   return func_words
# func_words=get_func_words()

# def uni_sent_encoder(stud_ans):
#   # Reduce logging output.
#   tf.logging.set_verbosity(tf.logging.ERROR)
#   module_url = "./uni_encoder" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
#   embed = hub.Module(module_url)
#   with tf.Session() as session:
#     session.run([tf.global_variables_initializer(), tf.tables_initializer()])
#     embeddings = session.run(embed(stud_ans))
#   return embeddings


# def cs_univ_encoder(stud_ans,ref_ans):
#     t=[]
#     t=stud_ans[:]
#     t.append(ref_ans)
#     matrix = uni_sent_encoder(t)
#     cossim_use=[0] * (len(matrix)-1)
#     for i in range(len(matrix)-1):
#         cossim_use[i] = 1 - spatial.distance.cosine(matrix[i], matrix[len(matrix)-1])
#     return cossim_use

# def word_sent_length(stud_ans):

#     sent_length=[0] * len(stud_ans)
#     av_word_length=[0] * len(stud_ans)
#     j=0
#     for i in stud_ans:
#         sent_length[j]=len(tokenizer.tokenize(i))
#         for w in i:
#             if(w!=' '):
#                 av_word_length[j]+=1
#         av_word_length[j]/=sent_length[j]
#         j+=1

#     ws = [av_word_length, sent_length]
#     return ws

# def avsenlen(stud_ans):
#     temp = word_sent_length(stud_ans)
#     avg_sent_length_in_doc = 0
#     for i in range(len(temp[1])):
#         avg_sent_length_in_doc += temp[1][i]
#     avg_sent_length_in_doc /= len(temp[1])
#     return avg_sent_length_in_doc

# def prompt_overlap(s_ans,question):
# #     print(len(tokenizer.tokenize(s_ans)),"\n",s_ans,'\n',question)
# #     overlap_metric = [0] * len(tokenizer.tokenize(s_ans))
#     qs_words = tokenizer.tokenize(question)
#     q_words = [w for w in qs_words if w not in stop_words]
#     l=0
#     overlap_metric = 0
#     w  = tokenizer.tokenize(s_ans)
#     for j in w:
#         for k in q_words:
#             if(j==k):
#                 overlap_metric+=1
#                 break
#         l+=1
#     myInt = len(q_words)
#     overlap_metric /= myInt
#     return overlap_metric

# def pre_word2vec():
#     model = r"enwiki_20180420_100d.txt"
#     word_vectors = gensim.models.KeyedVectors.load_word2vec_format(model, binary=False)
#     return word_vectors
# w2vmodel = pre_word2vec()

# def cosine_sim_word2vec(stud_ans,ref_ans):
#     nums=[]
#     for i in range(len(stud_ans)):
#         ss1 = stud_ans[i]
#         ss2 = ref_ans
#         data = []
#         data2= []

#         stop_words = set(stopwords.words('english'))
#         s1 = [w.lower() for w in tokenizer.tokenize(ss1) if w.lower() not in stop_words]
#         s2 = [w.lower() for w in tokenizer.tokenize(ss2) if w.lower() not in stop_words]

#         dd=[]
#         dd.append(s1)
#         dd.append(s2)


#         sim=0
#         for i in s1:
#             maxi=0
#             for j in s2:
#         #         print("I'm in")
#                 maxi = max(maxi,w2vmodel.similarity(i,j))
#             sim+=maxi

#         length = max(len(word_tokenize(ss1)), len(word_tokenize(ss2)))
#         sim/=length
#         nums.append(sim)
#     return nums

# def d2v(sa):
#     doc1=sa
#     docs = []
#     analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
#     for i, text in enumerate(doc1):
#         words = text.lower().split()
#         tags = [i]
#         docs.append(analyzedDocument(words, tags))

#     # Train model (set min_count = 1, if you want the model to work with the provided example data set)

#     model = doc2vec.Doc2Vec(docs, vector_size = 12, window = 300, min_count = 1, workers = 4)
#     return model.docvecs

# def cosine_sim_d2v(stud_ans,ref_ans):
#     t=[]
#     t=stud_ans[:]
#     t.append(ref_ans)
#     matrix = d2v(t)
#     cossimw2v=[0] * (len(matrix)-1)
#     for i in range(len(matrix)-1):
#         cossimw2v[i] = 1 - spatial.distance.cosine(matrix[i], matrix[len(matrix)-1])
#     return cossimw2v

# def IDFpp(stud_ans):
#     doc_info = []
#     j=0
#     for i in stud_ans:
#         j+=1
#         sa = tokenizer.tokenize(i)
#         count = len(sa)
#         temp = {"doc_id":j, "doc_length(count)":count}
#         doc_info.append(temp)

#     k=0
#     freq = []
#     for i in stud_ans:
#         k+=1
#         sa = tokenizer.tokenize(i)
#         fd={}
#         for w in sa:
#             w=w.lower()
#             if w in fd:
#                 fd[w]+=1
#             else:
#                 fd[w]=1
#             temp = {'doc_id':i, "freq":fd}
#         freq.append(temp)
#     #print(freq,"\n\n\n\n\n")
#     return doc_info, freq

# #Tfidf vectorizer function
# def IDF(stud_ans):
#     doc_info, freq = IDFpp(stud_ans)
#     IDFscore=[]
#     counter = 0

#     for d in freq:
#         counter+=1
#         for k in d['freq'].keys():
#             #print(k)
#             count = sum([k in tempDict['freq'] for tempDict in freq])
#             #if()
#             #print(count)
#             temp = {'doc_id':counter, 'IDFscore':math.log(len(doc_info)/count),'TF score':(count),'key':k}

#             IDFscore.append(temp)

#     return IDFscore

# def fsts(stud_ans,ref_ans):

#     k1=1.2
#     b=0.75
#     fstsvalue=[]
#     avsenlength = avsenlen(stud_ans)
#     #compare stud_ans and ref_ans
#     idfscore = IDF(stud_ans)
#     for i in range(len(stud_ans)):

#         if(len(word_tokenize(stud_ans[i])) > len(word_tokenize(ref_ans))):
#             lsen = [w.lower() for w in tokenizer.tokenize(stud_ans[i])]
#             ssen = [w.lower() for w in tokenizer.tokenize(ref_ans)]
#             sl=len((stud_ans[i]))
#             ss=len((ref_ans))
#         else:
#             ssen = [w.lower() for w in tokenizer.tokenize(stud_ans[i])]
#             lsen = [w.lower() for w in tokenizer.tokenize(ref_ans)]
#             ss=len((stud_ans[i]))
#             sl=len((ref_ans))
#         temp=0
#         for i in (lsen):
#             maxi=0
#             idf=0
#             for w in (ssen):
#                 maxi = max(maxi,w2vmodel.similarity(i,w))

#             for j in range(len(idfscore)):
#                 if(idfscore[j]['key'] == i):
#                     idf = idfscore[j]['IDFscore']


#             temp += idf * (maxi * (k1+1))
#             temp /= (maxi + k1* (1- b + b*(ss/avsenlength)))
#         fstsvalue.append(temp)
#     return fstsvalue

# def noun_overlap(stud_ans,ref_ans):

#     word_tokens = tokenizer.tokenize(stud_ans)

#     ref_tokens =  tokenizer.tokenize(ref_ans)


#     stud_ans_tag=nltk.pos_tag(word_tokens)
#     ref_ans_tag=nltk.pos_tag(ref_tokens)
#     ref_nouns=[]
#     stud_ans_nouns=[]
#     #use regex here
#     for i,j in ref_ans_tag:
#         if(j in ["NN","NNS","NNP","NNPS"]):
#             ref_nouns.append(i)
#     for i,j in stud_ans_tag:
#         if(j in ["NN","NNS","NNP","NNPS"]):
#             stud_ans_nouns.append(i)
#     score=0
#     for i in stud_ans_nouns:
#         if i in ref_nouns:
#             score=score+1;
#     return score/len(ref_nouns)

# def content_overlap(s,r):#both are lists

#     s_ans=[]
#     ref_ans=r
#     t=[]
#     for i in range(len(s)):
#         t=(tokenizer.tokenize(s[i]))
#         s_ans.append(t)
#     for i in range(len(s_ans)):
#         s_ans[i] = [lemmatizer.lemmatize(j) for j in s_ans[i] if j not in func_words]
#     ref_ans = [lemmatizer.lemmatize(i) for i in tokenizer.tokenize(ref_ans) if i not in func_words]
#     length=len(ref_ans)
#     for i in range(len(ref_ans)):
#         for j in wn.synsets(ref_ans[i]):
#             for k in j.lemmas():
#                 ref_ans.append(k.name())
#     temp=[]
#     for i in s_ans:
#         val=0
#         for j in i:
#             if j in ref_ans:
#                 val+=1
#         temp.append(val/(length))
#     return temp

# def lsa_score(stud_ans):
#       corpus = [ans for ques in stud_ans for ans in ques]
#       vectorizer = TfidfVectorizer(min_df = 1, stop_words = 'english')
#       dtm = vectorizer.fit_transform(corpus)
#       lsa = TruncatedSVD(3, algorithm = 'arpack')
#       dtm=dtm.astype(float)
#       dtm_lsa = lsa.fit_transform(dtm)
#       dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)
#       lsa_stud=pd.DataFrame(dtm_lsa, index = corpus, columns = ["component_1","component_2",'component_3'])
#       X=[]
#       for i in range(len(corpus)):
#         t=[]
#         t.append(lsa_stud.iloc[i,:1].values[0])
#         t.append(lsa_stud.iloc[i,1:2].values[0])
#         t.append(lsa_stud.iloc[i,2:3].values[0])
#         X.append(t)
#       return X

# def elmo_vectors(x):
#     # Create graph and finalize (optional but recommended).
#     g = tf.Graph()
#     with g.as_default():
#       text_input = tf.placeholder(dtype=tf.string, shape=[None])
#       elmo = hub.Module("./elmo_module", trainable=True)
#       embeddings = elmo(x, signature="default", as_dict=True)["elmo"]
#       init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
#     # g.finalize()
#     # Create session and initialize.
#     session = tf.Session(graph=g)
#     session.run(init_op)
#     return session.run(tf.reduce_mean(embeddings,1))
#     # embeddings = elmo(x, signature="default", as_dict=True)["elmo"]
#     #
#     # with tf.Session() as sess:
#     #     sess.run(tf.global_variables_initializer())
#     #     sess.run(tf.tables_initializer())
#     #
#     #     # return average of ELMo features
#     #     return sess.run(tf.reduce_mean(embeddings,1))

# def cos_sim_elmo(stud_ans,ref_ans):
#     t=[]
#     t=stud_ans[:]
#     t.append(ref_ans)
#     matrix = elmo_vectors(t)
#     cossimelmo = [0] * (len(matrix))
#     for i in range(len(matrix)):
#         cossimelmo[i] = 1 - spatial.distance.cosine(matrix[i], matrix[len(matrix)-1])
#     return cossimelmo

# def jc_sim(stud_ans,ref_ans):
#   X=[]
#   c=0
#   ref_words=tokenizer.tokenize(ref_ans)
#   ref_words=[lemmatizer.lemmatize(j) for j in ref_words if j.lower() not in stop_words]
#   for s in stud_ans:
#     num=0
#     words=tokenizer.tokenize(s)
#     words=[lemmatizer.lemmatize(j) for j in words if j.lower() not in stop_words]
#     l=max(len(ref_words),len(words))
#     for w in words:
#       maxi=0
#       for w1 in wn.synsets(w):
#         for t in ref_words:
#           for w2 in wn.synsets(t):
#             if w1._pos in ('n','v','a','r') and w2._pos in ('n','v','a','r') and w1._pos==w2._pos:
#               n=w1.jcn_similarity(w2,genesis_ic)
#               if w1==w2 or n>1:
#                 maxi=1
#               else:
#                 maxi=max(maxi,w1.jcn_similarity(w2,genesis_ic))
#       num=num+maxi
#     num=num/l
#     X.append(num)
#   return X

# def sp_sim(stud_ans,ref_ans):
#   X=[]
#   c=0
#   ref_words=tokenizer.tokenize(ref_ans)
#   ref_words=[lemmatizer.lemmatize(j) for j in ref_words if j.lower() not in stop_words]
#   for s in stud_ans:
#     num=0
#     words=tokenizer.tokenize(s)
#     words=[lemmatizer.lemmatize(j) for j in words if j.lower() not in stop_words]
#     l=max(len(ref_words),len(words))
#     for w in words:
#       maxi=0
#       for w1 in wn.synsets(w):
#         for t in ref_words:
#           for w2 in wn.synsets(t):
#             if w1._pos in ('n','v','a','r') and w2._pos in ('n','v','a','r') and w1._pos==w2._pos:
#               n=w1.lch_similarity(w2,genesis_ic)
#               #print(w1, w2, type(n), n)
#               #return None when there is no similarity hence needed to add another if clause
#               if n == None:
#                 maxi=0
#               elif w1==w2 or n>1:
#                 maxi=1
#               else:
#                 maxi=max(maxi,w1.lch_similarity(w2,genesis_ic))
#       num=num+maxi
#       #print(num)
#     num=num/l

#     X.append(num)
#   return X


# def ttr(sent):
#     words=tokenizer.tokenize(sent)
#     return len(set(words))/len(words)

# def calc_train_features():
#   X=[]
#   lss=lsa_score(stud_ans)
#   c=0
#   for i in range(len(stud_ans)):
#     sta=stud_ans[i]
#     ref=ref_ans[i]
#     que=question[i]
#     lt=len(sta)
#     wsn=word_sent_length(sta)
#     csw2v=cosine_sim_word2vec(sta,ref)
#     csd2v=cosine_sim_d2v(sta,ref)
#     fs=fsts(sta,ref)
#     co = content_overlap(sta,ref)
#     cselmo = cos_sim_elmo(sta, ref)
#     jcs = jc_sim(sta,ref)
#     sps = sp_sim(sta,ref)
#     csuse = cs_univ_encoder(sta,ref)
#     for j in range(lt):
#         temp = []
#         temp.append(prompt_overlap(sta[j],que))
#         for k in range(1):
#             temp.append(wsn[k][j])
#         temp.append(csw2v[j])
#         temp.append(csd2v[j])
#         temp.append(fs[j])
#         # temp.append(noun_overlap(sta[j],ref))
#         # temp.append(co[j])
#         for k in range(3):
#           temp.append(lss[c][k])
#         temp.append(ttr(sta[j]))
#         temp.append(jcs[j])
#         temp.append(sps[j])
# #         temp.append(glv[j])
#         temp.append(csuse[j])
#         X.append(temp)
#         print(i," - ",j, " -- ",c)
#         c=c+1


# def get_features(sta,ref,q):
#   temps=stud_ans[:]
#   temps.append(sta)
#   lss=lsa_score(temps)[-len(sta):]
#   wsn=word_sent_length(sta)
#   csw2v=cosine_sim_word2vec(sta,ref)
#   csd2v=cosine_sim_d2v(sta,ref)
#   fs=fsts(sta,ref)
#   co = content_overlap(sta,ref)
#   cselmo = cos_sim_elmo(sta, ref)
#   jcs = jc_sim(sta,ref)
#   sps = sp_sim(sta,ref)
#   csuse = cs_univ_encoder(sta,ref)
#   X=[]
#   for j in range(len(sta)):
#     temp=[]
#     temp.append(prompt_overlap(sta[j],q))
#     for k in range(1):
#         temp.append(wsn[k][j])
#     temp.append(csw2v[j])
#     temp.append(csd2v[j])
#     temp.append(fs[j])
#     # temp.append(noun_overlap(sta[j],ref))
#     # temp.append(co[j])
#     temp.append(cselmo[j])
#     for k in range(3):
#       temp.append(lss[j][k])
#     temp.append(ttr(sta[j]))
#     temp.append(jcs[j])
#     temp.append(sps[j])
#     temp.append(csuse[j])
#     X.append(temp)
#   return X

# def train_data():
#   xdf=pd.read_csv("./final_features.csv")[['prompt_overlap','avg_word_length','cosineword2vec','cosinedoc2vec','fsts','cosine_elmo','lsa1','lsa2','lsa3','ttr','jc_sim','sps','cs_use','score']]
#   Y=xdf['score'].values
#   xdf=xdf.drop(['score'],axis=1)
#   X=xdf.values
#   return X,Y

# def train_model():
#   X,Y=train_data()
#   train_x, test_x, train_y, test_y = train_test_split(X,Y,test_size=0.2)
#   clf = RandomForestClassifier(n_estimators=120,max_depth=15)
#   clf.fit(train_x,train_y)
#   print( "Test Accuracy  :: ", accuracy_score(test_y, clf.predict(test_x)))
#   return clf

# clf=train_model()

# def predict_ans(X):
#     return clf.predict(X)

# def get_prob(X):
#     return clf.predict_proba(X)