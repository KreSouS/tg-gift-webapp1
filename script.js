let balance = 0;
let gifts = ["🌟 Суперподарок", "🎈 Воздушный шар", "🧸 Мишка", "🍫 Шоколадка", "🧨 Пусто"];

const tg = window.Telegram.WebApp;
const user_id = tg.initDataUnsafe.user.id;

function updateUI() {
  document.getElementById("balance").innerText = balance;
}

function earnCoins() {
  const earned = Math.floor(Math.random() * 5) + 1;
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

async function fetchBalance() {
  try {
    const response = await fetch("http://localhost:8080/get_balance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ user_id: user_id })
    });

    const data = await response.json();
    if (data.balance !== undefined) {
      balance = data.balance;
      updateUI();
    } else {
      alert("Ошибка при получении баланса");
    }
  } catch (error) {
    console.error("Ошибка запроса:", error);
    alert("Сервер не отвечает");
  }
}

// Загружаем баланс при запуске
fetchBalance();

