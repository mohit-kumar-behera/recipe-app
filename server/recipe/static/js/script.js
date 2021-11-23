const openModalBtns = document.querySelectorAll('.modal-opener');
const closeModalBtns = document.querySelectorAll('.modal-closer');
console.log(closeModalBtns);

const openModal = elem => {
  document.querySelector(`.${elem}`).style.display = 'flex';
};

const closeModal = elem => {
  document.querySelector(`.${elem}`).style.display = 'none';
};

openModalBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const openEl = btn.dataset.open;
    openModal(openEl);
  });
});

closeModalBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const closeEl = btn.dataset.close;
    closeModal(closeEl);
  });
});
