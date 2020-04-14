<html>
<head>
    <title>预约美签，防止失学</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/style/bootstrap.min.css">
    <link rel="stylesheet" href="/style/bootstrap-theme.min.css">
    <script src="/style/jquery.min.js"></script>
    <script src="/style/bootstrap.min.js"></script>
    <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
	<script src="/style/echarts.min.js"></script>
    <style type='text/css'>
    .table thead tr th { text-align: center; vertical-align: middle; }
    .table tbody tr td { text-align: center; vertical-align: middle; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="span12">
<h1 class="text-center" id="title">预约时间变化单日统计图</h1><br>
<?php
$y = $_GET['y'];
$m = $_GET['m'];
$d = $_GET['d'];
if (is_numeric($y) && is_numeric($m) && is_numeric($d))
	$date = $y.'/'.$m.'/'.$d;
else
	$date = date("Y/m/d", time());
$loc = ['北京', '成都', '广州', '上海', '沈阳'];
$raw = [];
$data = [];
$x = [];
foreach ($loc as $name) {
	$tmp = explode("\n", file_get_contents('../'.$name.'/'.$date));
	$raw[$name] = [];
	foreach ($tmp as $info) {
		$tm = explode(' ', $info)[0];
		if ($tm != '') {
			$raw[$name][$tm] = explode(' ', $info)[1];
			if (!in_array($tm, $x)) array_push($x, $tm);
		}
	}
}
sort($x);
$n = count($x);
foreach ($loc as $name) {
	$data[$name] = [];
	for ($i = 0; $i < $n; ++$i) $data[$name][$i] = $raw[$name][$x[$i]];
	for ($i = $n - 1; $i >= 0; --$i) {
		$j = $raw[$name][$x[$i]];
		if ($j == null && $i > 0)
			$j = $data[$name][$i - 1];
		$data[$name][$i] = $j;
	}
}
 ?>
				<center>
<div id="chart" style="height: 400px; width: '100%'"></div>
<script type="text/javascript">
var c = echarts.init(document.getElementById('chart'));
var o = {
title: {text: "<?php echo substr($date, 5) ?>"},
tooltip: {
	trigger: 'axis',
	formatter: function(data) {
		var result = data[0].name + '<br/>';
		for (var i = 0, length = data.length; i < length; ++i) {
			result += data[i].marker + data[i].seriesName + ': ' + data[i].data + '<br>';
		}
		return result;
	}
},
legend: {data: <?php echo json_encode($loc); ?>},
//toolbox: {feature: {saveAsImage: {}}},
xAxis: {type: 'category', boundaryGap: false, data: <?php echo json_encode($x); ?>},
yAxis: {type: 'time'},
series: [
<?php
foreach ($loc as $name) {
	echo '{name: "'.$name.'", type: "line", data: '.json_encode($data[$name]).'},'."\n";
}
 ?>
]
};
c.setOption(o);
</script>
<?php
$d = new Datetime($date);
$pre = explode('/', $d->modify("-1 day")->format("Y/m/d"));
echo '<a class="btn btn-info" role="button" href="/visa2/view/?y='.$pre[0].'&m='.$pre[1].'&d='.$pre[2].'">前一天</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
echo '<a class="btn btn-info" role="button" href="/visa">返回首页</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
$nxt = explode('/', $d->modify("+2 day")->format("Y/m/d"));
echo '<a role="button" class="btn btn-info" href="/visa2/view/?y='.$nxt[0].'&m='.$nxt[1].'&d='.$nxt[2].'">后一天</a>';
?>
				</center>
</div></div></div>
</body>
</html>
