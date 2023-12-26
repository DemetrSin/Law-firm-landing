function updateContent(langData) {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        // Сохраняем значение атрибута data-i18n в переменной key
        let key = element.getAttribute('data-i18n');
        // Проверяем, равен ли значение атрибута data-i18n строке 'name_placeholder'
        if (element.getAttribute('data-i18n') === 'name_placeholder') {
            // Устанавливаем атрибут placeholder элемента со значением из объекта langData соответствующей строки
            element.setAttribute('placeholder', langData[key]);
        }
        // Проверяем, равен ли значение атрибута data-i18n строке 'message_placeholder'
        if (element.getAttribute('data-i18n') === 'message_placeholder') {
            // Устанавливаем атрибут placeholder элемента со значением из объекта langData соответствующей строки
            element.setAttribute('placeholder', langData[key]);
        } else (
            // Устанавливаем textContent элемента с помощью соответствующего значения из объекта langData
            element.textContent = langData[key])


    });
}


// Function to set the language preference
function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
    location.reload();
}

// Function to fetch language data
async function fetchLanguageData(lang) {
    const response = await fetch(`static/languages/${lang}.json`);

    return response.json();
}

// Function to change language
async function changeLanguage(lang) {
    await setLanguagePreference(lang);

    const langData = await fetchLanguageData(lang);
    updateContent(langData);
}

// Call updateContent() on page load
window.addEventListener('DOMContentLoaded', async () => {
    const userPreferredLanguage = localStorage.getItem('language') || 'en';
    const langData = await fetchLanguageData(userPreferredLanguage);
    updateContent(langData);
});