/* 轮播图函数*/
function startCarousel(carouselId, interval) {
    const carousel = document.getElementById(carouselId);
    const carouselInner = carousel.querySelector('.carousel-inner');
    const images = carouselInner.querySelectorAll('img');
    let currentIndex = 0;

    function showNextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        carouselInner.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    setInterval(showNextImage, interval);
}

document.addEventListener('DOMContentLoaded', () => {
    startCarousel('carouselTop', 3000); // 3秒轮播一次
    startCarousel('carouselBottom', 3000); // 3秒轮播一次
});

/* lora信息展示监听 */
document.getElementById('contentSelectTop').addEventListener('change', function() {
var selectedOption = this.options[this.selectedIndex]; // 获取当前选中的选项对象
var displayTextElement = document.getElementById('displayTextTop');

if (selectedOption.value !== "") {
    // 根据选项的value属性查找对应的文本内容
    switch (selectedOption.value) {
    case 'option1':
        displayTextElement.textContent = '这是选项1对应的详细信息。';
        break;
    case 'option2':
        displayTextElement.textContent = '这是选项2对应的详细信息。';
        break;
    case 'option3':
        displayTextElement.textContent = '这是选项3对应的详细信息。';
        break;
    default:
        // 处理默认情况，尽管在上述switch-case中已经排除了空字符串的情况，这里可以省略
        break;
    }
} else {
    // 如果没有选择任何选项，清空文本显示
    displayTextElement.textContent = '';
}
});

/* model信息展示监听 */
document.getElementById('contentSelectBottom').addEventListener('change', function() {
var selectedOption = this.options[this.selectedIndex]; // 获取当前选中的选项对象
var displayTextElement = document.getElementById('displayTextBottom');

if (selectedOption.value !== "") {
    // 根据选项的value属性查找对应的文本内容
    switch (selectedOption.value) {
    case 'option1':
        displayTextElement.textContent = '这是model1信息。';
        break;
    case 'option2':
        displayTextElement.textContent = '这是model2信息。';
        break;
    case 'option3':
        displayTextElement.textContent = '这是model3信息。';
        break;
    default:
        // 处理默认情况，尽管在上述switch-case中已经排除了空字符串的情况，这里可以省略
        break;
    }
} else {
    // 如果没有选择任何选项，清空文本显示
    displayTextElement.textContent = '';
}
});