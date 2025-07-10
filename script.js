let balance = 0;
let gifts = ["🌟 Суперподарок", "🎈 Воздушный шар", "🧸 Мишка", "🍫 Шоколадка", "🧨 Пусто"];

function updateUI() {
  document.getElementById("balance").innerText = balance;
}

function earnCoins() {
  const earned = Math.floor(Math.random() * 5) + 1; // 1–5 монет
  balance += earned;
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
