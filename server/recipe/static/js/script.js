const openModalBtns = document.querySelectorAll('.modal-opener');
const closeModalBtns = document.querySelectorAll('.modal-closer');

const setElemDisplay = (elem, displayState) => {
  document.querySelector(`.${elem}`).style.display = displayState;
};

const openModal = elem => {
  document.body.style.overflow = 'hidden';
  setElemDisplay(elem, 'flex');
};

const closeModal = elem => {
  document.body.style.overflow = 'auto';
  setElemDisplay(elem, 'none');
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
