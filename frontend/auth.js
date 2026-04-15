const poolData = {
  UserPoolId: "ap-south-1_O5WuVlgnP",
  ClientId: "11kigi99f79mj6lh7v742q70cn"
};

const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

// Signup
function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  userPool.signUp(email, password, [], null, (err, result) => {
    if (err) {
      alert(err.message);
      return;
    }
    alert("Signup successful! Please login.");
  });
}
function confirmUser() {
  const email = document.getElementById("email").value;
  const otp = document.getElementById("otp").value;

  const userData = {
    Username: email,
    Pool: userPool
  };

  const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

  cognitoUser.confirmRegistration(otp, true, function(err, result) {
    if (err) {
      alert(err.message);
      return;
    }
    alert("Account confirmed! Now login.");
  });
}
// Login
function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const authDetails = new AmazonCognitoIdentity.AuthenticationDetails({
    Username: email,
    Password: password
  });

  const userData = {
    Username: email,
    Pool: userPool
  };

  const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

  cognitoUser.authenticateUser(authDetails, {
    onSuccess: function (result) {
      const token = result.getIdToken().getJwtToken();

      localStorage.setItem("token", token);

      alert("Login successful!");
      window.location.href = "dashboard.html";
    },
    onFailure: function (err) {
      alert(err.message);
    }
  });
}