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
  
def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map
  
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
    st.title("Map with binary variable and time-series")
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
    #选择需要的特征
    varibles=tuple(df.columns.tolist())
    metric_df = pd.DataFrame(
    with st.sidebar:
      option = st.selectbox('Which variable',varibles)
    # 添加数据点到地图
    for i, row in df.iterrows():
        if row[option] == 1:
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
     
    
