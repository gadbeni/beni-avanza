// selecciona la barra de navegación
const navbar = document.querySelector('.navbar');

// escucha el evento de scroll en la página
window.addEventListener('scroll', () => {
  // obtiene la posición actual de desplazamiento
  const scrollPosition = window.scrollY;

  // si el usuario ha desplazado más allá de la altura de la barra de navegación, agrega la clase de CSS para cambiar el estilo de la barra de navegación
  if (scrollPosition > navbar.offsetHeight) {
    navbar.classList.add('navbar-scrolled');
  } else {
    // de lo contrario, quita la clase de CSS para volver al estilo original de la barra de navegación
    navbar.classList.remove('navbar-scrolled');
  }
});