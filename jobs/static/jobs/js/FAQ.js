const faqSections = document.querySelectorAll('.faq-section');

faqSections.forEach(section => {
  const plusIcon = section.querySelector('.plus-icon');
  const answer = section.querySelector('.faq-answer');

  plusIcon.addEventListener('click', () => {
    if (answer.style.display === 'none') {
      answer.style.display = 'block';
      plusIcon.textContent = '-';
    } else {
      answer.style.display = 'none';
      plusIcon.textContent = '+';
    }
  });
});
