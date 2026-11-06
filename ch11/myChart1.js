let ctx = null;
let chart = null;
let config = {
    // type은 차트 종류 지정
    type: 'bar', /* line 등으로 바꿀 수 있음 */

    // data는 차트에 출력될 전체 데이터 표현
    data: {
        // labels는 배열로 데이터의 레이블들
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],

        // datasets 배열로 차트에 그려질 모든 데이터 셋 표현.
        // 아래는 그래프 1개만 있는 경우
        datasets: [{
            label: '2026년',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'yellow',
            borderWidth: 2,
            data: [5, 10, 5, 2, 20, 30, 45], // 각 레이블에 해당하는 데이터
            fill: true // 그래프에 색을 채울지 지정
        }]
    },

    // 차트의 속성 지정
    options: {
        responsive : false, // 웹 브라우저의 크기에 따른 크기 조절 금지
        scales: { // x축과 y축 정보
            x: { // x축
                display: true,
                title: { display: true, text: '계절' }, // 축 이름
            },
            y: { // y축
                display: true,
                title: { display: true, text: '선호도(%)' }, // 축 이름
                min: 0, // y 축 최소 눈금
                max: 100, // y축 최대 눈금
                ticks : { stepSize: 10 }
            },
        }
    }
};

function drawChart() { // Chart 객체 생성 및 차트 그리기
   ctx = document.getElementById('canvas').getContext('2d');
   chart = new Chart(ctx, config); // Chart 객체 생성. 캔버스에 차트 그려짐
}

function change(month, value) { // 첫 막대의 이름을 month로 바꾸고 값을 value로 변경
   chart.data.labels[0] = month; // 첫 막대의 이름을 month로 변경
   chart.data.datasets[0].data[0] = value; // 첫 막대의 값을 value로 변경
   chart.update() // 갱신된 차트를 화면에 다시 그림
}

function add(label, value) { // 그래프에 label 이름의 새로운 막대 삽입. 값 value로 설정
   chart.data.labels.push(label); // 새 막대의 이름을 labels[] 배열의 끝에 추가
   chart.data.datasets[0].data.push(value); // 새 막대의 값을 data[] 배열의 끝에 추가
   chart.update(); // 갱신된 차트를 화면에 다시 그림
}

function remove() { // 그래프에서 맨 앞 막대 제거
   chart.data.labels.shift(); // labels[] 배열에서 맨 앞 원소 제거
   chart.data.datasets[0].data.shift(); // data[] 배열에서 맨 앞 원소 제거
   chart.update(); // 갱신된 차트를 화면에 다시 그림
}
