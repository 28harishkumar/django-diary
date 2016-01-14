$(document).ready(function(){
	$('.navbar-brand').mouseenter(function(){
		if(window.innerWidth < 768){
			return false;
		}
		$('.g-menu').css('display','block');
	});

	$('.page-name-btn').click(function(e){
		e.preventDefault();
		$('.g-menu').toggle('slow');
	});

	$('.g-menu').mouseleave(function(){
		if(window.innerWidth < 768){
			return false;
		}
		$('.g-menu').css('display','none');
	});

	$('.navbar-toggle').click(function(){
		$('.g-menu').toggle();
	});

	$('.container').css('margin-top','60px');
});