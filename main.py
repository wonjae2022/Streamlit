import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import matplotlib.dates as mdates 
import pydeck as pdk   


st.title('Visualization Project')
st.subheader('기후 시나리오에 따른 시군구별 작물 생육 적합도')



with st.form(key='Form2'):
    with st.sidebar:
        yearslider = st.sidebar.slider('년도',1981,2100)
        location_selectbox = st.selectbox('시군구',('강릉','강화','거제','거창','고흥','광주','구미','군산','금산','남원','남해','대관령','대구','대전','목포','문경','밀양','보령','보은','부산','부안','부여','산청','서귀포','서산','서울','성산','속초','수원','양평','여수','영덕','영주','영천','완도','울산','울진','원주','의성','이천','인제','인천','임실','장흥','전주','정읍','제주','제천','진주','천안','청주','추풍령','춘천','충주','통영','포항','합천','해남','홍천'))
        cultiva_selectbox = st.selectbox('작물',('단감','당귀','배','복숭아','사과','인삼','천궁','포도'))
        submitted2 = st.form_submit_button(label = 'submit')


st3 = pd.read_csv('st3.csv')
df_13 = pd.read_csv((st3[st3['kEname']==location_selectbox]['number']+'_new2.csv').values[0])
df_14= df_13[df_13['Year']==yearslider]
max2012 = df_14['tmax'].mean()
min2012 = df_14['tmin'].mean()
fruit2 = pd.read_csv('fruit2.csv', encoding = 'cp949')
fruit2_1 = fruit2[fruit2['작물명']== cultiva_selectbox]['연평균 최고기온'].values[0]
fruit2_2 = fruit2[fruit2['작물명']== cultiva_selectbox]['연평균 최저기온'].values[0]

if (max2012 >= fruit2_1) & (min2012 <= fruit2_2):
    first_score = 100
    nansu1 = np.exp(abs(max2012 - fruit2_1)/10) 
    nansu2 = np.exp(abs(min2012 - fruit2_2)/10)
    nansu = nansu1 + nansu2
    total_score = first_score - nansu
elif (max2012 <= fruit2_1) & (min2012 >= fruit2_2):
    first_score = 100
    total_score = first_score
elif (max2012 >= fruit2_1) & (min2012 >= fruit2_1):
    first_score = 0
    total_score = first_score
elif (max2012 <= fruit2_2) & (min2012 <= fruit2_2):
    first_score = 0
    total_score = first_score
elif (max2012<=fruit2_1) & (max2012>=fruit2_2) & (min2012<= fruit2_2):
    first_score = (max2012-fruit2_2)/(fruit2_1 - fruit2_2)*100
    nansu1 = np.exp(abs(min2012 - fruit2_2)/10)
    if nansu1 >= first_score:
        tscore = 0
    else:
        tscore = first_score - nansu1
    total_score = tscore
else:
    first_score = (fruit2_1-min2012)/(fruit2_1 - fruit2_2)*100
    nansu1 = np.exp(abs(max2012 - fruit2_1)/10) 
    if nansu1 >= first_score:
        tscore = 0
    else:
        tscore = first_score - nansu1
    total_score=tscore

####################################
st3 = pd.read_csv('st3.csv')
fruit2 = pd.read_csv('fruit2.csv', encoding = 'cp949')
fruit2_1 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 최고기온'].values[0]
fruit2_2 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 최저기온'].values[0]
fruit2_3 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 시작'].values[0]
fruit2_4 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 끝'].values[0]
df_13 = pd.read_csv((st3[st3['kEname']==location_selectbox]['number']+'_new2.csv').values[0])
df_130 = df_13[df_13['Year']==yearslider]
if (fruit2_4-fruit2_3) == 2:
    df_131 = df_130[df_130['Mon']==fruit2_3]
    df_132 = df_130[df_130['Mon']==fruit2_3+1]
    df_231 = df_130[df_130['Mon']==fruit2_4]
    df_133 = pd.concat([df_131,df_132,df_231])  
elif (fruit2_4-fruit2_3) == 4:
    df_131 = df_130[df_130['Mon']==fruit2_3]
    df_132 = df_130[df_130['Mon']==fruit2_3+1]
    df_1321 = df_130[df_130['Mon']==fruit2_3+2]
    df_1322 = df_130[df_130['Mon']==fruit2_3+3]
    df_231 = df_130[df_130['Mon']==fruit2_4]
    df_133 = pd.concat([df_131,df_132,df_1321, df_1322, df_231])
else :
    df_131 = df_130[df_130['Mon']==fruit2_3]
    df_132 = df_130[df_130['Mon']==fruit2_3+1]
    df_1321 = df_130[df_130['Mon']==fruit2_3+2]
    df_1322 = df_130[df_130['Mon']==fruit2_3+3]
    df_1323 = df_130[df_130['Mon']==fruit2_3+4]
    df_1324 = df_130[df_130['Mon']==fruit2_3+5]
    df_231 = df_130[df_130['Mon']==fruit2_4]
    df_133 = pd.concat([df_131,df_132,df_1321, df_1322,df_1323, df_1324, df_231])
df_133 = df_133.reset_index()
tavgmin = []
tavgmax = []
for i in range(len(df_133)):
    tavgmin.append(fruit2_2)
    tavgmax.append(fruit2_1)
df_134 = pd.concat([df_133,pd.Series(tavgmin).rename('생육 최저기온'),pd.Series(tavgmax).rename('생육 최고기온')],axis = 1)

max2013 = df_134['tmax'].mean()
min2013 = df_134['tmin'].mean()

if (max2013 >= fruit2_1) & (min2013 <= fruit2_2):
    first_score = 100
    nansu1 = np.exp(abs(max2013 - fruit2_1)/10) 
    nansu2 = np.exp(abs(min2013 - fruit2_2)/10)
    nansu = nansu1 + nansu2
    total_score2 = first_score - nansu
elif (max2013 <= fruit2_1) & (min2013 >= fruit2_2):
    first_score = 100
    total_score2 = first_score
elif (max2013 >= fruit2_1) & (min2013 >= fruit2_1):
    first_score = 0
    total_score2 = first_score
elif (max2013<=fruit2_1) & (max2013>=fruit2_2) & (min2013<= fruit2_2):
    first_score = (max2013-fruit2_2)/(fruit2_1 - fruit2_2)*100
    nansu1 = np.exp(abs(min2013 - fruit2_2)/10)
    total_score2 = first_score - nansu1
else:
    first_score = (fruit2_1-min2013)/(fruit2_1 - fruit2_2)*100
    nansu1 = np.exp(abs(max2013 - fruit2_1)/10) 
    total_score2 = first_score - nansu1

data_frame2 = {'total_score' : round(total_score,2),'nonscore' : 100-round(total_score,2)}
data_frame3 = {'total_score2' : round(total_score2,2),'nonscore' : 100-round(total_score2,2)}
data_frame4 = {'total_score3' : round((round(total_score2,2)+round(total_score,2))/2,2),'nonscore' : 100-round(((round(total_score2,2)+round(total_score,2))/2))}
data_frame = {'score' : 70,'nonscore' : 30}

st3 = pd.read_csv('st3.csv')
col1, col2 = st.columns([3,2])
if data_frame4['total_score3'] >= 90:
    get_color='[0, 0, 100, 160]'
elif data_frame4['total_score3'] >= 70:
    get_color='[0, 100, 0, 160]'
elif data_frame4['total_score3'] >= 45:
    get_color='[195, 195, 0, 160]'
elif data_frame4['total_score3'] >= 25:
    get_color='[255, 140, 0, 160]'
elif data_frame4['total_score3'] > 0:
    get_color='[100, 0, 0, 160]'
else :
    get_color='[0, 0, 0, 160]'
with col1:
    st35 = st3[st3['kEname'] == location_selectbox][['Lat','Lon']]
    st35.columns = ['lat','lon']
    st35 = st35.reset_index(drop = True)
    st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=36.4,
        longitude=127.78,
        zoom=6,
        pitch=10,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=st35,
            get_position='[lon, lat]',
            get_color=get_color,
            get_radius=7000,
        ),
    ],
    ))
with col2:
    image = Image.open('legend.png')
    image2 = Image.open(cultiva_selectbox + '2.jpg')
    st.image(image)
    st.image(image2)



col1_1, col1_2 = st.columns([2,1])
with col1_1:
    fig = plt.figure(1)
    ax = fig.add_subplot()
    if data_frame4['total_score3'] >= 90:
        colors = ['blue','white']
    elif data_frame4['total_score3'] >= 70:
        colors = ['green','white']
    elif data_frame4['total_score3'] >= 45:
        colors = ['yellow','white']
    elif data_frame4['total_score3'] >= 25:
        colors = ['orange','white']
    elif data_frame4['total_score3'] >= 0:
        colors = ['red','white']
    else:
        colors = ['black','white']
    ax.pie([data_frame4['total_score3'],data_frame4['nonscore']],colors = colors, explode = (0.05,0.05))
    centre_circle = plt.Circle((0, 0), 0.84, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.text(-0.,0,data_frame4['total_score3'], size = 20, horizontalalignment='center', verticalalignment='center')
    plt.title('Total', size = 20)
    st.pyplot(fig)
with col1_2:
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot()
    if data_frame2['total_score'] >= 90:
        colors = ['blue','white']
    elif data_frame2['total_score'] >= 70:
        colors = ['green','white']
    elif data_frame2['total_score'] >= 45:
        colors = ['yellow','white']
    elif data_frame2['total_score'] >= 25:
        colors = ['orange','white']
    else:
        colors = ['red','white']
    ax2.pie([data_frame2['total_score'],data_frame2['nonscore']],colors = colors, explode = (0.05,0.05))
    centre_circle = plt.Circle((0, 0), 0.90, fc='white')
    fig2.gca().add_artist(centre_circle)
    ax2.text(-0.,0,data_frame2['total_score'], size = 20, horizontalalignment='center', verticalalignment='center')
    plt.title('Year', size = 20)
    st.pyplot(fig2)

    fig3 = plt.figure(3)
    ax3 = fig3.add_subplot()
    if data_frame3['total_score2'] >= 90:
        colors = ['blue','white']
    elif data_frame3['total_score2'] >= 70:
        colors = ['green','white']
    elif data_frame3['total_score2'] >= 45:
        colors = ['yellow','white']
    elif data_frame3['total_score2'] >= 25:
        colors = ['orange','white']
    else:
        colors = ['red','white']
    ax3.pie([data_frame3['total_score2'],data_frame3['nonscore']],colors = colors, explode = (0.05,0.05))
    centre_circle = plt.Circle((0, 0), 0.90, fc='white')
    fig3.gca().add_artist(centre_circle)
    ax3.text(-0.,0,data_frame3['total_score2'], size = 20, horizontalalignment='center', verticalalignment='center')
    plt.title('Growth', size = 20)
    st.pyplot(fig3)


#st.subheader(location_selectbox + '의 최고기온, 최저기온')
#st3 = pd.read_csv('st3.csv')
#df = pd.read_csv((st3[st3['kEname']==location_selectbox]['number']+'_new2.csv').values[0])
#df2 = df.groupby('Year').max()['tmax']
#df3 = df.groupby('Year').min()['tmin']
#df4 = pd.concat([df2,df3], axis = 1)
#fig = plt.figure(figsize=(11,4))
#plt.plot(df4['tmax'], color = 'red')
#plt.plot(df4['tmin'], color = 'blue')
#plt.legend(['tmax','tmin'])
#st.pyplot(fig)
st.subheader('연도에 따른 ' + location_selectbox + '에서의 ' + cultiva_selectbox + ' 재배 점수')
dfdf1 = pd.read_csv(cultiva_selectbox + '_총점.csv')
fig = plt.figure(figsize = (11,4))
plt.plot(dfdf1[location_selectbox], color = 'black')
plt.axhline(90, 0.05, 0.95, color='blue', linestyle='--', linewidth=1)
plt.axhline(70, 0.05, 0.95, color='green', linestyle='--', linewidth=1)
plt.axhline(45, 0.05, 0.95, color='yellow', linestyle='--', linewidth=1)
plt.axhline(25, 0.05, 0.95, color='orange', linestyle='--', linewidth=1)
plt.axhline(0, 0.05, 0.95, color='red', linestyle='--', linewidth=1)
plt.xticks(range(0,121,10), range(1980,2101,10))
plt.ylabel('Total Score')
st.pyplot(fig)










st.subheader(cultiva_selectbox + '의 적정 연간평균 기온과 ' + location_selectbox + '의 연간 기온 비교')
st3 = pd.read_csv('st3.csv')
fruit2 = pd.read_csv('fruit2.csv', encoding = 'cp949')
fruit2_1 = fruit2[fruit2['작물명']== cultiva_selectbox]['연평균 최저기온']
fruit2_2 = fruit2[fruit2['작물명']== cultiva_selectbox]['연평균 최고기온']
df = pd.read_csv((st3[st3['kEname']==location_selectbox]['number']+'_new2.csv').values[0])
tavgmin = []
tavgmax = []
for i in range(len(df)):
    tavgmin.append(fruit2_1.values[0])
    tavgmax.append(fruit2_2.values[0])
df1_1 = pd.concat([df,pd.Series(tavgmin).rename('연평균 최저기온'),pd.Series(tavgmax).rename('연평균 최고기온')],axis = 1)
df2 = df1_1.groupby('Year').mean()[['tmax','tmin','연평균 최저기온','연평균 최고기온']] 
fig = plt.figure(figsize=(11,4))
plt.plot(df2['tmax'], color = 'red')
plt.plot(df2['tmin'], color = 'blue')
plt.plot(df2['연평균 최저기온'], color = 'lightgray')
plt.plot(df2['연평균 최고기온'], color = 'lightgray')
plt.axvline(yearslider, 0, 1, color='#FFCC33', linestyle='--', linewidth=2)
plt.legend(['tmax','tmin','optimal_tmin','optimal_tmax'], loc = 'upper left')
plt.fill_between(x = df2.index, y1= df2['연평균 최저기온'],y2 =df2['tmin'], where = df2['tmin'] < df2['연평균 최저기온'],interpolate= True,  facecolor = 'blue', alpha = 0.5)
plt.fill_between(x = df2.index, y1= df2['연평균 최고기온'],y2 =df2['tmax'], where = df2['tmax'] > df2['연평균 최고기온'],interpolate= True,  facecolor = 'red', alpha = 0.5)
plt.fill_between(x = df2.index, y1= df2['연평균 최고기온'],y2 =df2['tmin'], where = df2['tmin'] > df2['연평균 최고기온'],interpolate= True,  facecolor = 'white', alpha = 1)
plt.fill_between(x = df2.index, y1= df2['연평균 최저기온'],y2 =df2['tmax'], where = df2['tmax'] < df2['연평균 최저기온'],interpolate= True,  facecolor = 'white', alpha = 1)
st.pyplot(fig)

# st.subheader(cultiva_selectbox + '의 적정 연간평균 기온과 ' + location_selectbox + '의 특정 연도 기온 비교')
# st3 = pd.read_csv('st3.csv')
# df = pd.read_csv((st3[st3['kEname']==location_selectbox]['number']+'_new2.csv').values[0])
# df2_1 = df[df['Year']==yearslider]
# df2_1 = df2_1.reset_index()
# fruit2 = pd.read_csv('fruit2.csv', encoding = 'cp949')
# fruit2_1 = fruit2[fruit2['작물명']== cultiva_selectbox]['연평균 최저기온']
# fruit2_2 = fruit2[fruit2['작물명']== cultiva_selectbox]['연평균 최고기온']
# tavgmin = []
# tavgmax = []
# for i in range(len(df2_1)):
#     tavgmin.append(fruit2_1.values[0])
#     tavgmax.append(fruit2_2.values[0])
# df2_2 = pd.concat([df2_1,pd.Series(tavgmin).rename('연평균 최저기온'),pd.Series(tavgmax).rename('연평균 최고기온')],axis = 1)
# dfodf = []
# for i in range(len(df2_2)):    
#     dfodf.append(str(df2_2['Mon'][i]) + '/'+str(df2_2['Day'][i]))
# df2_2['date'] = dfodf
# fig = plt.figure(figsize=(11,4))
# plt.plot(df2_2['tmax'], color = 'red')
# plt.plot(df2_2['tmin'], color = 'blue')
# plt.plot(df2_2['연평균 최저기온'], color = 'lightgray')
# plt.plot(df2_2['연평균 최고기온'], color = 'lightgray')
# plt.xticks(np.arange(0,365,15), labels = ['Jan','','Feb','','Mar','','Apr','','May','','Jun','','Jul','','Aug','','Sep','','Oct','','Nov','','Dec','',''])
# plt.fill_between(x = df2_2.index, y1= df2_2['연평균 최저기온'],y2 =df2_2['tmin'], where = df2_2['tmin'] < df2_2['연평균 최저기온'],interpolate= True,  facecolor = 'blue', alpha = 0.5)
# plt.fill_between(x = df2_2.index, y1= df2_2['연평균 최고기온'],y2 =df2_2['tmax'], where = df2_2['tmax'] > df2_2['연평균 최고기온'],interpolate= True,  facecolor = 'red', alpha = 0.5)
# plt.fill_between(x = df2_2.index, y1= df2_2['연평균 최고기온'],y2 =df2_2['tmin'], where = df2_2['tmin'] > df2_2['연평균 최고기온'],interpolate= True,  facecolor = 'white', alpha = 1)
# plt.fill_between(x = df2_2.index, y1= df2_2['연평균 최저기온'],y2 =df2_2['tmax'], where = df2_2['tmax'] < df2_2['연평균 최저기온'],interpolate= True,  facecolor = 'white', alpha = 1)
# st.pyplot(fig)

################################################################
st.subheader('')
st.subheader(cultiva_selectbox + ' 생육시기에서 적정 생육 기온과 ' + location_selectbox + '의 기온 비교')
st3 = pd.read_csv('st3.csv')
fruit2 = pd.read_csv('fruit2.csv', encoding = 'cp949')
fruit5_1 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 최저기온']
fruit5_2 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 최고기온']
fruit5_3 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 시작']
fruit5_4 = fruit2[fruit2['작물명']== cultiva_selectbox]['생육 끝']
df_13 = pd.read_csv((st3[st3['kEname']==location_selectbox]['number']+'_new2.csv').values[0])
df_130 = df_13[df_13['Year']==yearslider]
if (fruit5_4.values[0]-fruit5_3.values[0]) == 2:
    df_131 = df_130[df_130['Mon']==fruit5_3.values[0]]
    df_132 = df_130[df_130['Mon']==fruit5_3.values[0]+1]
    df_231 = df_130[df_130['Mon']==fruit5_4.values[0]]
    df_133 = pd.concat([df_131,df_132,df_231])  
elif (fruit5_4.values[0]-fruit5_3.values[0]) == 4:
    df_131 = df_130[df_130['Mon']==fruit5_3.values[0]]
    df_132 = df_130[df_130['Mon']==fruit5_3.values[0]+1]
    df_1321 = df_130[df_130['Mon']==fruit5_3.values[0]+2]
    df_1322 = df_130[df_130['Mon']==fruit5_3.values[0]+3]
    df_231 = df_130[df_130['Mon']==fruit5_4.values[0]]
    df_133 = pd.concat([df_131,df_132,df_1321, df_1322, df_231])
else :
    df_131 = df_130[df_130['Mon']==fruit5_3.values[0]]
    df_132 = df_130[df_130['Mon']==fruit5_3.values[0]+1]
    df_1321 = df_130[df_130['Mon']==fruit5_3.values[0]+2]
    df_1322 = df_130[df_130['Mon']==fruit5_3.values[0]+3]
    df_1323 = df_130[df_130['Mon']==fruit5_3.values[0]+4]
    df_1324 = df_130[df_130['Mon']==fruit5_3.values[0]+5]
    df_231 = df_130[df_130['Mon']==fruit5_4.values[0]]
    df_133 = pd.concat([df_131,df_132,df_1321, df_1322,df_1323, df_1324, df_231])
df_133 = df_133.reset_index()
tavgmin = []
tavgmax = []
for i in range(len(df_133)):
    tavgmin.append(fruit5_1.values[0])
    tavgmax.append(fruit5_2.values[0])
df_134 = pd.concat([df_133,pd.Series(tavgmin).rename('생육 최저기온'),pd.Series(tavgmax).rename('생육 최고기온')],axis = 1)
fig = plt.figure(figsize=(11,4))
plt.plot(df_134['tmax'], color = 'red')
plt.plot(df_134['tmin'], color = 'blue')
plt.plot(df_134['생육 최저기온'], color = 'lightgray')
plt.plot(df_134['생육 최고기온'], color = 'lightgray')
if fruit5_4.values[0]-fruit5_3.values[0] == 2:
    plt.xticks(np.arange(0,((fruit5_4.values[0]-fruit5_3.values[0])+1)*30,15), labels = ['Mar','','Jun','','Jul',''])

elif fruit5_4.values[0]-fruit5_3.values[0] == 4:
    plt.xticks(np.arange(0,((fruit5_4.values[0]-fruit5_3.values[0])+1)*30,15), labels = ['Mar','','Jun','','Jul','','Aug','','Sep',''])
else:
    plt.xticks(np.arange(0,((fruit5_4.values[0]-fruit5_3.values[0])+1)*30,15), labels = ['Apr','','Mar','','Jun','','Jul','','Aug','','Sep','','Oct',''])
plt.fill_between(x = df_134.index, y1= df_134['생육 최저기온'],y2 =df_134['tmin'], where = df_134['tmin'] < df_134['생육 최저기온'],interpolate= True,  facecolor = 'blue', alpha = 0.5)
plt.fill_between(x = df_134.index, y1= df_134['생육 최고기온'],y2 =df_134['tmax'], where = df_134['tmax'] > df_134['생육 최고기온'],interpolate= True,  facecolor = 'red', alpha = 0.5)
plt.fill_between(x = df_134.index, y1= df_134['생육 최고기온'],y2 =df_134['tmin'], where = df_134['tmin'] > df_134['생육 최고기온'],interpolate= True,  facecolor = 'white', alpha = 1)
plt.fill_between(x = df_134.index, y1= df_134['생육 최저기온'],y2 =df_134['tmax'], where = df_134['tmax'] < df_134['생육 최저기온'],interpolate= True,  facecolor = 'white', alpha = 1)
st.pyplot(fig)

###########################################################################
xxx= []
for i in np.arange(1981,2101, 10):
    xxx.append(i)
    for j in range(9):
        xxx.append('')
        
st.subheader('')
st.subheader(location_selectbox + '에서 ' + cultiva_selectbox + ' 생육 기간간 점수')   
heatmap = pd.read_csv(location_selectbox+'_'+cultiva_selectbox+'.csv')
heatmap.index = heatmap['Year']
del heatmap['Year']
fig, ax = plt.subplots(figsize=(25, 10))
im = ax.matshow(heatmap.T, cmap='Greens')
ax.set_xticks(np.arange(len(heatmap.T.columns)), labels=xxx, size = 10)
ax.set_yticks(np.arange(len(heatmap.T.index)), labels=heatmap.T.index, size = 10)
ax.grid(False)
fig.colorbar(im)
st.pyplot(fig)

col2_1, col2_2 = st.columns([3,2])
with col2_2:
    st.text('서울대학교 농생명공학부 이노현, 정원재')

