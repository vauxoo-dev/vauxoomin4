openerp.log_info = function(instance) {
instance.web.client_actions.add('log.info.action', 'instance.log_info_action');
    instance.log_info_action = instance.web.Widget.extend({
        template : 'log_info_template',
        start:function(){
            url_split = window.location.href.split('&');
            console.log(url_split)
            var nopasa = false;
            for (i=0; i <= url_split.length; i++){
                if (url_split[i] == 'active_id%5B%5D=999'){
                    nopasa = true;
                }
            }
            if (!nopasa){
            window.location.href += '&active_id=999';
            window.location.reload()
            }
            $('#war').on('click',
                        function(eve){
                                     $('.showtag').removeClass('showtag')
                                     $('#warnings').addClass('showtag')});
            $('#err').on('click',
                        function(eve){
                                     $('.showtag').removeClass('showtag')
                                     $('#errors').addClass('showtag')});
            $('#in').on('click',
                        function(eve){
                                     $('.showtag').removeClass('showtag')
                                     $('#info').addClass('showtag')});
            $('#test').on('click',
                        function(eve){
                                     $('.showtag').removeClass('showtag')
                                     $('#tests').addClass('showtag')})
        },
            });
};
