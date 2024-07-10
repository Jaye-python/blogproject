
function showPasswordLogin() {
    $('#togglePasswordLogin').on('click', function() {
      var passwordField = $('#id_password');
      var type = passwordField.attr('type') === 'password' ? 'text' : 'password';
      passwordField.attr('type', type);
  
      $(this).toggleClass('bi bi-eye-slash-fill'); 
      $(this).toggleClass('bi bi-eye-fill'); 
    });
  };

  function showPassword() {
    $('#togglePassword').on('click', function() {
      var passwordField = $('#id_password1');
      var type = passwordField.attr('type') === 'password' ? 'text' : 'password';
      passwordField.attr('type', type);
  
      $(this).toggleClass('bi bi-eye-slash-fill');
      $(this).toggleClass('bi bi-eye-fill'); 
    });
  };
  
  function showPassword2() {
    $('#togglePassword2').on('click', function() {
      var passwordField = $('#id_password2');
      var type = passwordField.attr('type') === 'password' ? 'text' : 'password';
      passwordField.attr('type', type);
  
      $(this).toggleClass('bi bi-eye-slash-fill'); 
      $(this).toggleClass('bi bi-eye-fill'); 
      
    });
  };

function loadCategories() {
    $.ajax({
        url: "/loadcategories/",
        method: "GET",
        success: function(data) {
            var select = $('#loadcategories');
            select.empty();
            select.append('<option value="">-----</option>');
            $.each(data, function(index, category) {
                select.append('<option value="' + category.name + '">' + category.name + '</option>');
            });
        }
    });
}