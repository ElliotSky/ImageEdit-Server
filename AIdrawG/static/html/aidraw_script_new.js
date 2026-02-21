/* 按键监听 */
// 点击上传文件：展示隐藏按键
document.getElementById('customUploadButton').addEventListener('click', function() {
    console.log('开始触发预览图更新');
    document.getElementById('uploadImageButton').click();
    document.getElementById('actionButtons').classList.remove('hidden');
});

// 上传文件处理
let isDetectionCompleted = false;
document.getElementById('uploadImageButton').addEventListener('change', function(event) {
    console.log('开始预览图更新逻辑');
    var file = event.target.files[0];
    if (file) {
        var allowedTypes = ['image/jpeg','image/jpg', 'image/png']; // 允许的图片类型数组
        // 检查文件类型是否在允许范围内
        if (allowedTypes.indexOf(file.type) === -1) {
            alert('请选择一个图片文件！');
            return; // 如果不是图片类型，直接返回，不再继续执行
        }

        console.log('文件已选择:', file.name);
        isDetectionCompleted = false;
        // 这里可以继续编写处理文件的代码，如读取文件数据进行预览等
        var reader = new FileReader(); 
        reader.onload = function(e) { 
          // 文件读取成功时设置img的src为读取到的数据URL 
          document.getElementById('previewImage').src = e.target.result; 
          // 可选：清除原有的alt文本或设置为其他描述 
          document.getElementById('previewImage').alt = file.name; 
        }; // 开始读取文件 
        reader.readAsDataURL(file); 
    }
});




    /*  按键逻辑区 */
    // 图片与提示词检测函数
    function checkupdata() {
        let imageFile = document.getElementById('uploadImageButton').files[0];
        if (!imageFile) {
            alert('请先上传一张图片！');
            return;
        }
        let userInput = prompt('请输入提示词:', '');
        if (userInput === null || userInput.trim() === '') {
            alert('请输入有效的提示词！');
            return;
        }
        return { imageFile, userInput };
    }

     
    // 目标检测数据上传函数new
    function uploadForDetection(file, userInput) {
      return new Promise((resolve, reject) => {
        const url = 'http://scientist.ink/jsonvim/'; 
        const formData = new FormData();
        formData.append('file', file, file.name); // 文件，文件名
        formData.append('userInput', userInput); // 用户输入的提示词
        formData.append('tasktype', 'detection'); // 指定任务类型为检测

        fetch(url, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('服务器响应:', data);
            if(data.imageindex) {
                alert('目标检测完成！');
                resolve(data.imageindex);
            } else {
                alert(data.error || '未知错误');
                // reject(data.error || '未知错误');
            }
        })
        .catch(error => {
            console.error('请求错误:', error);
            alert('文件上传或目标检测时出错！');
            // reject(error); // 将错误传递给外部
        });
      });
    }

    // 基于检测结果上传进行图像生成数据上传函数new
    function uploadForGeneration(imageIndex, userInput, loraName, modelName, boxes) {   
        return new Promise((resolve, reject) => {
            const url = 'http://scientist.ink/jsonvim/'; 
            const formData = new FormData();
            formData.append('imageindex', imageIndex); // 从检测得到的图像索引
            formData.append('prompt', userInput);
            formData.append('loraname', loraName); // LORA名称
            formData.append('modelname', modelName); // 模型名称
            formData.append('boxes', JSON.stringify(boxes)); // 检测框信息，可能为"autoboxes"或具体的坐标数据
            formData.append('tasktype', 'generation'); // 指定任务类型为生成

            fetch(url, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('服务器响应:', data);
                if(data.gerenImg_url) {
                    resolve(data.gerenImg_url);
                    alert('图像生成任务执行成功！');
                } else {
                    alert(data.error || '未知错误');
                }
            })
            .catch(error => {
                console.error('请求错误:', error);
                alert('发送生成任务请求时出错！');
            });
        });
    }

    // // 预览图逻辑
    function startCheckingForUpdates0(imageIndex, retryCount = 0, maxRetries = 5) {
        let imageUrlBase = `http://scientist.ink/data/detect_output2/${imageIndex}`;
        let timestamp = new Date().getTime();
        let imageUrl = `${imageUrlBase}?_=${timestamp}`;
    
        // 创建一个新的Image对象
        let img = new Image();
    
        // 设置图片加载成功的回调
        img.onload = function() {
            document.getElementById('previewImage').src = imageUrl; // 图片加载完成后更新预览图片的src
            console.log("图片加载成功");
        };
    
        // 设置图片加载失败的回调
        img.onerror = function() {
            console.log("图片加载成功");
            if (retryCount < maxRetries) {
                setTimeout(() => {
                    startCheckingForUpdates0(imageIndex, retryCount + 1, maxRetries);
                }, 2000); // 例如，等待2秒后重试
                console.log("图片重载",retryCount,"次");
            } else {
                console.error("图片加载失败，已达到最大重试次数。");
                // 这里可以处理最终失败的情况，比如显示一个错误消息或默认图片
            }
            console.error("图片加载失败，请检查图片URL是否正确或图片是否存在。");
        };
    
        // 开始加载图片
        img.src = imageUrl;
    }
    function startCheckingForUpdates(imageIndex) {
        // let encodedFilename = encodeURIComponent(filename);
        // 获取文件名不带扩展名的部分
        // let baseName = encodedFilename.slice(0, encodedFilename.lastIndexOf('.'));
        
        let imageUrlBase = `http://scientist.ink/data/detect_output${imageIndex}`;

        let timestamp = new Date().getTime();
        let imageUrl = `${imageUrlBase}?_=${timestamp}`;
        document.getElementById('previewImage').src = imageUrl; // 更新图片URL
    }
    // 右侧预览图逻辑
    function startCheckingserverImage(imageIndex) {
        // 确保图片元素存在再进行操作
        let imageUrlBase0 = `http://scientist.ink/data/geren_output/0${imageIndex}`;
        let imageUrlBase1 = `http://scientist.ink/data/geren_output/1${imageIndex}`;
        
        // 更新第一个图片的URL
        let timestamp = new Date().getTime();
        let imageUrl0 = `${imageUrlBase0}?_=${timestamp}`;
        let imageUrl1 = `${imageUrlBase1}?_=${timestamp}`;
        // document.getElementById('previewImage').src = imageUrl; // 更新图片URL
        document.getElementById('serverImage0').src = imageUrl0;
        document.getElementById('serverImage1').src = imageUrl1;

        document.getElementById('serverImage1').style.display = 'block';
    }
    

    /* 手动画框 按键1 */
    function getActualBoxes(){
      return false;
    }
    // document.getElementById('handdetect').addEventListener('click', function() {
    //   alert('功能待完善'); // 弹出提示框显示"功能待完善"
    //   // getActualBoxes();
    // });

    let imageIndexurl;
    
    /* 自动检测 按键2*/
    document.getElementById('autodetect').addEventListener('click', function() {
        let { imageFile, userInput } = checkupdata();
        startCheckingForUpdates0(imageFile.name)
        uploadForDetection(imageFile, userInput) // 传递文件和用户输入到上传函数
            .then(imageIndex => {
                imageIndexurl=imageIndex
                isDetectionCompleted=true;
                startCheckingForUpdates(imageIndexurl)
                console.log('Image Index:', imageIndex);
            })
            .catch(error => {
                console.error('Error during detection:', error);
                isDetectionCompleted=false;
            });
    });

    /* 图像生成 按键3 */
    document.getElementById('generateButton').addEventListener('click', function() {
      if (!isDetectionCompleted) {
        alert('请先完成目标检测！');
        return;
      }
      let userInput = prompt('请输入提示词:', '');
      if (userInput === null || userInput.trim() === '') {
          alert('请输入有效的提示词！');
      }
      // 获取lora和model的选中值
      let loraName = document.getElementById('contentSelectTop').value;
      let modelName = document.getElementById('contentSelectBottom').value;
      let boxes = isDetectionCompleted ? getActualBoxes() : [];
      // 确保所有必需的变量都有值再进行下一步
      if (imageIndexurl && userInput && loraName && modelName) {
            uploadForGeneration(imageIndexurl, userInput, loraName, modelName, boxes)
                .then(gerenImg_url => {
                    startCheckingserverImage(gerenImg_url)
                    console.log('Image Index:', gerenImg_url);
                })
                .catch(error => {
                    console.error('Error during detection:', error);
                });
            
      } else {
          alert('缺少必要的数据，请检查上传的图片和选择的选项！');
      }
      
    });