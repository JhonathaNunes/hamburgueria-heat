$(function ($) {
    $(function() {
        const maskBehavior = function (value) {
            return value.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
        }

        phoneOptions = {
            onKeyPress: function(_, _, field, options) {
                field.mask(maskBehavior.apply({}, arguments), options);
            }
        };

        $('#phone').mask(maskBehavior, phoneOptions);
        $('#cpf').mask('000.000.000-00');
        $('#cep').mask('00000-000');
        $('#number #quantity').mask('0#');
        $('#price').mask('##.000,00', { reverse: true });
    });
});