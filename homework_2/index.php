<h1>乘法计算器</h1>
<form action="" method="post">

    <h2>第一个数：</h2>
    <input type="text" name="num1">
    <h2>第二个数：</h2>
    <input type="text" name="num2">
    <br />
    <br />
    <input type="submit" name="submit" value="计算">
</form>
<h3>相乘结果：</h3>
<?php
$num1 = 0;
$num2 = 0;
if(isset($_POST['num1']) && $_POST['num1']!="")
{
    $num1 = $_POST['num1'];
    
}

if(isset($_POST['num2']) && $_POST['num2']!="")
{
    $num2 = $_POST['num2'];
    
}

echo $num1*$num2;
?>
