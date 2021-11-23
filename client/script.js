document.getElementById('login-btn').addEventListener('click',
  function () {
    document.querySelector('.login-modal').style.display = 'flex';
  });

document.getElementById('signup-btn').addEventListener('click',
  function () {
    document.querySelector('.signup-modal').style.display = 'flex';
  });

document.querySelector('.close').addEventListener('click', function () {
  document.querySelector('.login-modal').style.display = 'none';
})

document.querySelector('.close-btn').addEventListener('click', function () {
  document.querySelector('.signup-modal').style.display = 'none';
})