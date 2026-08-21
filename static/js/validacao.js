$(document).ready(function () {

    $(".form-valida-senha").on("submit", function (evento) {
        var formulario = $(this);

        formulario.find(".js-erro-senha").remove();

        var campoSenha = formulario.find("[name='senha'], [name='nova_senha']").first();
        var campoConfirmar = formulario.find("[name='confirmar_senha'], [name='confirmar_nova_senha']").first();

        var senha = campoSenha.val();
        var confirmar = campoConfirmar.val();

        if (campoSenha.length && campoConfirmar.length && (senha || confirmar)) {
            if (senha !== confirmar) {
                evento.preventDefault();
                $("<p class='js-erro-senha' style='color:#a12626; font-weight:bold;'>As senhas digitadas não são iguais.</p>")
                    .insertAfter(campoConfirmar);
                campoConfirmar.trigger("focus");
            }
        }
    });

    $("input[name='email']").on("blur", function () {
        var campo = $(this);
        var valor = campo.val().trim();
        var regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        campo.next(".js-erro-email").remove();

        if (valor && !regexEmail.test(valor)) {
            campo.after("<small class='js-erro-email' style='color:#a12626; display:block; margin-top:0.2em;'>Digite um e-mail válido.</small>");
        }
    });

    $("input[name='cpf']").on("blur", function () {
        var campo = $(this);
        var apenasNumeros = campo.val().replace(/\D/g, "");

        campo.next(".js-erro-cpf").remove();

        if (apenasNumeros && apenasNumeros.length !== 11) {
            campo.after("<small class='js-erro-cpf' style='color:#a12626; display:block; margin-top:0.2em;'>O CPF deve ter 11 números.</small>");
        }
    });

    $("input[name='foto']").on("change", function (evento) {
        var arquivo = evento.target.files[0];
        var preview = $("#preview-foto");

        if (arquivo && preview.length) {
            var leitor = new FileReader();
            leitor.onload = function (e) {
                preview.attr("src", e.target.result);
                preview.removeClass("preview-foto-oculta");
            };
            leitor.readAsDataURL(arquivo);
        }
    });

});
