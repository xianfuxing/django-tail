$(document).ready(function(){
// 标记导航区域的current项目
  $('.navbar-nav li a').each(function(){
      //if(location.href == this.href) {
      if(location.href.indexOf(this.href) > -1 && this.pathname != '/' ) {
        $(this).parent('li').addClass('active');
      }

      if(location.href.indexOf(this.href) > -1 && this.pathname == '/' && location.pathname == '/') {
        $(this).parent('li').addClass('active');
      }
  });
});
