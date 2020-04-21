<?php
header("Access-Control-Allow-Origin: *");
$t = $_POST["t"];
$s = file_get_contents('state');
if ($s == '1' and strlen($t) == 5) {
	$handle = fopen('state', 'w');
	fwrite($handle, $t);
	fclose($handle);
	$s = $t;
}
 ?>
<html>
<head>
	<title>预约美签，防止失学</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="/style/bootstrap.min.css">
	<link rel="stylesheet" href="/style/bootstrap-theme.min.css">
	<script src="/style/jquery.min.js"></script>
	<script src="/style/bootstrap.min.js"></script>
	<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
    <style type='text/css'>
	.table thead tr th { text-align: center; vertical-align: middle; }
	.table tbody tr td { text-align: center; vertical-align: middle; }
    </style>
</head>
<body>
	<div class="container">
		<div class="row">
			<div class="span12">
				<h1 class="text-center" id="title">
					爬虫状态
				</h1>
	<center>
	<br>
	（如果看到它连续两个小时没刷新的话，或者有新的Feature Request，可以去<a href="https://github.com/Trinkle23897/us-visa">GitHub</a>上提issue）
	<br>
	<br>
<?php
echo "当前状态：".file_get_contents('state').'，<a href="/visa">点击返回</a><br><br>';
echo '<table class="table table-hover table-striped table-bordered"><thead><tr><th>F1/J1</th><th>B1/B2</th><th>H1B</th></tr></thead><tbody><tr><td>'.json_decode(file_get_contents('../visa/visa.json'), true)['time'].'</td><td>'.json_decode(file_get_contents('../visa/visa-b.json'), true)['time'].'</td><td>'.json_decode(file_get_contents('../visa/visa-h.json'), true)['time'].'</td></tr></tbody></table>';
?>
广告位招租，详情咨询：<a href="https://trinkle23897.github.io/">https://trinkle23897.github.io/</a><br><br>
	</center>
<div id="disqus_thread"></div>
<script>
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = 'https://tuixue-online.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<br>
			</div>
		</div>
	</div>

</html>
