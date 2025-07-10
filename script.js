let balance = 0;
let gifts = ["🌟 Суперподарок", "🎈 Воздушный шар", "🧸 Мишка", "🍫 Шоколадка", "🧨 Пусто"];

function updateUI() {
  document.getElementById("balance").innerText = balance;
}

function earnCoins() {
  const earned = Math.floor(Math.random() * 6) + 5; // 5–10 монет
  balance += earned;

  // Отправляем данные боту
  Telegram.WebApp.sendData(JSON.stringify({ reward: earned }));

  alert(`Вы получили ${earned} монет!`);
  updateUI();
}

function openCase() {
  if (balance < 10) {
    alert("Недостаточно монет!");
    return;
  }
  balance -= 10;
  const gift = gifts[Math.floor(Math.random() * gifts.length)];
  document.getElementById("history").innerHTML += `<li>${gift}</li>`;
  updateUI();
}

updateUI();

