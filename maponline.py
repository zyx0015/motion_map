###包的导入
import folium
import pandas as pd
import streamlit as st
import numpy as np
import streamlit_folium
from streamlit_folium import st_folium

############functions#############
def filter_sites_by_era(file, current_time):
    input_df=pd.read_csv(file,encoding="gbk")
    # 确保输入数据合法性
    if 'Upper' not in input_df.columns or 'Lower' not in input_df.columns:
        raise ValueError("输入数据表格缺少'Upper'或'Lower'列")
    # 使用布尔索引筛选出符合条件的遗址
    filtered_df = input_df[(input_df['Lower'] <= current_time) & (input_df['Upper'] >= current_time)]
    return filtered_df

marker_colors = [
    'red',
    'blue',
    'orange',
    'gray',
    'darkred',
    'lightred',
    'beige',
    'green',
    'darkblue',
    'darkgreen',
    'lightblue',
    'lightgreen',
    'purple',
    'lightgray',
    'darkpurple',
    'pink',
    'cadetblue',
    'black'
]

############start##################
with st.sidebar:
    st.title("有段石锛")
    file_name = st.file_uploader("import your csv file")
    current_time = st.slider("BP",0,8000,5000,100)

if file_name is not None:
    #写一个函数，读取csv并且根据时间筛选
    df = filter_sites_by_era(file_name,current_time)  # 读取上传的 CSV 文件
    # 创建地图对象
    m = folium.Map(location=[df['Lat'].mean(), df['Lon'].mean()],
                   zoom_start=5,
                  )
    # 添加数据点到地图
    cultures=list(set(df['Culture']))
    color_set=marker_colors[:len(cultures)]
    colordict=dict(zip(cultures,color_set))
    # 添加数据点到地图
    for i, row in df.iterrows():
        if row['有段石锛'] == 1:
            folium.CircleMarker(
            [row['Lat'], row['Lon']],
            radius=5,
            color='black',
            fill_color=colordict[row['Culture']],
            fill=True,
            fill_opacity=1
            ).add_to(m)
        else:
            folium.CircleMarker(
            [row['Lat'], row['Lon']],
            radius=5,
            color='b',
            fill_color='grey',
            fill=True,
            fill_opacity=0.2
            ).add_to(m)
    #添加图例
    m = add_categorical_legend(m, 'legend',
                             colors = color_set,
                           labels = cultures)
    st_folium(m,width=1000)
    st.dataframe(df) 
     
    
