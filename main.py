import streamlit as st
import requests
import json
img_list = []
current_index = 0
max_retries = 3  # 设置最大重试次数
st.title('图片获取器-V3')
select_option = st.selectbox('选择一个图片源', ('Anosu', 'Jitsuの随机涩图', '选项3'))
selected_index = ['Anosu', 'Jitsuの随机涩图', '选项3'].index(select_option)
num_input = st.number_input('输入获取张数（最大100）', min_value=0, max_value=100, value=1)

def Restart(img_list):
    global image_path
    with open('./json/index.json', 'r') as index:
        i = json.load(index)
    image_path = img_list[i]
    if st.button('下一张'):
        if i >= 0:
            i = i - 1
            image_path = img_list[i]
            with open('./json/index.json', 'w') as json_file:
                json.dump(i, json_file)
        else:
            st.write('最后一张了好吧')

def Json(img_list):
    # 保存图片列表到 img.json 文件中
    global num_input
    file_path = './json/img.json'  # 文件路径和名称
    # 使用 with 语句打开文件，将图片列表写入 JSON 文件中
    with open(file_path, 'w') as json_file:
        json.dump(img_list, json_file)
    print(f"图片列表已保存到 {file_path} 文件中")
    with open('./json/index.json','w') as json_file:
        json.dump(num_input-1,json_file)
    st.experimental_rerun()

def Request_Retry(api_url):
    retries_index = 0
    while retries_index < max_retries:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                st.write(f'获取失败重试第{retries_index+1}次')
        except requests.RequestException as e:
            st.write(f"请求发生异常：{e}")
        retries_index += 1
    return None
def Anosu(num_input):
    r18 = st.selectbox('年龄分级',('关闭r18','开启r18','随机(50%)'))
    r18_index = ['关闭r18','开启r18','随机(50%)'].index(r18)
    size_options = ['original', 'regular', 'small']
    size = st.selectbox('选择图片尺寸', size_options)
    keyword = st.text_input('输入图片tags所包含的关键字')
    db = st.selectbox('使用的图库（数据库）', ('新图库','老图库'))
    db_index = ['新图库','老图库'].index(db)
    api_url = f'https://image.anosu.top/pixiv/json?num={num_input}&r18={r18_index}&size={size}&keyword={keyword}&db={db_index}'
    if st.button('开始获取'):
        data = Request_Retry(api_url)
        if data != None:
            i = 0
            while i < num_input:
                img_list = data[i]['url']
            print(img_list)
        else:
            st.write('超过最大重试次数，无法获取 JSON 数据')
            st.write(api_url)

def Jitsu(num_input):
    sort = st.selectbox('分类',('pixiv', 'r18', 'jitsu'))
    size = st.selectbox('规格',('original', 'regular', 'small', 'thumb', 'mini'))
    num = num_input
    api_url = f'https://moe.jitsu.top/api?sort={sort}&size={size}&num={num}&type=json'
    if st.button('开始获取'):
        data = Request_Retry(api_url)
        if data != None:
            img_list = data['pics']
            Json(img_list)
        else:
            st.write('超过最大重试次数，无法获取 JSON 数据')
            st.write(api_url)

with open('./json/img.json', 'r') as file:
    json_data = json.load(file)
if json_data is not None:
    img_list = json_data
# 获取所选选项的索引

if selected_index == 0:
    Anosu(num_input)
elif selected_index == 1:
    Jitsu(num_input)


if img_list is not None and len(img_list) > 0:
    Restart(img_list)
else:
    image_path = './img/example_image.jpg'


st.image(image_path, caption='图片预览', use_column_width=True)


if st.button('重置程序'):
    file_path = './json/img.json'  # 文件路径和名称
    # 使用 with 语句打开文件，将图片列表写入 JSON 文件中
    with open(file_path, 'w') as json_file:
        json.dump(None, json_file)
    st.write('程序已重置')
    st.experimental_rerun()