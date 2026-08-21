// ============================================================
// Validações feitas no NAVEGADOR (client-side) com jQuery.
//
// Importante: essas validações são só para dar um feedback mais
// rápido pro usuário, ANTES de enviar o formulário. Elas não
// substituem as validações que o Flask já faz no servidor
// (routes/cadastro.py, routes/perfil.py, routes/admin.py) -
// afinal, alguém mal-intencionado pode desligar o JavaScript e
// mandar a requisição do mesmo jeito. Por isso o servidor sempre
// confere tudo de novo.
// ============================================================

$(document).ready(function () {

    // ---- 1) Confere se "senha" e "confirmar senha" são iguais ----
    // Funciona em qualquer formulário que tenha a classe "form-valida-senha".
    // Aceita tanto o par senha/confirmar_senha (cadastro) quanto
    // nova_senha/confirmar_nova_senha (troca de senha no perfil/admin).
    $(".form-valida-senha").on("submit", function (evento) {
        var formulario = $(this);

        // remove um aviso antigo, se já existia de uma tentativa anterior
        formulario.find(".js-erro-senha").remove();

        var campoSenha = formulario.find("[name='senha'], [name='nova_senha']").first();
        var campoConfirmar = formulario.find("[name='confirmar_senha'], [name='confirmar_nova_senha']").first();

        var senha = campoSenha.val();
        var confirmar = campoConfirmar.val();

        // Só valida se os dois campos existirem e tiverem algo digitado
        // (no formulário de editar usuário do admin, por exemplo, a
        // troca de senha é opcional - pode ficar em branco)
        if (campoSenha.length && campoConfirmar.length && (senha || confirmar)) {
            if (senha !== confirmar) {
                evento.preventDefault();
                $("<p class='js-erro-senha' style='color:#a12626; font-weight:bold;'>As senhas digitadas não são iguais.</p>")
                    .insertAfter(campoConfirmar);
                campoConfirmar.trigger("focus");
            }
        }
    });

    // ---- 2) Confere formato básico de e-mail ao sair do campo ----
    $("input[name='email']").on("blur", function () {
        var campo = $(this);
        var valor = campo.val().trim();
        var regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        campo.next(".js-erro-email").remove();

        if (valor && !regexEmail.test(valor)) {
            campo.after("<small class='js-erro-email' style='color:#a12626; display:block; margin-top:0.2em;'>Digite um e-mail válido.</small>");
        }
    });

    // ---- 3) Confere se o CPF tem 11 números (sem validar dígito verificador) ----
    $("input[name='cpf']").on("blur", function () {
        var campo = $(this);
        var apenasNumeros = campo.val().replace(/\D/g, "");

        campo.next(".js-erro-cpf").remove();

        if (apenasNumeros && apenasNumeros.length !== 11) {
            campo.after("<small class='js-erro-cpf' style='color:#a12626; display:block; margin-top:0.2em;'>O CPF deve ter 11 números.</small>");
        }
    });

    // ---- 4) Pré-visualização da foto de perfil escolhida ----
    // Se a página tiver um <input type="file" name="foto"> e uma
    // <img id="preview-foto">, mostra a imagem escolhida na hora,
    // antes mesmo de enviar o formulário.
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
