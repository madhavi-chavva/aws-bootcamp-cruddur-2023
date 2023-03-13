# Week 3 — Decentralized Authentication

## Create Cognito user pool in AWS console.

![cognito user pool](https://user-images.githubusercontent.com/125069098/223254875-40245e32-01f3-47d8-8ae2-d6c1e58c9829.png)

## Install AWS AMPLIFY in the frontend-end-js folder
```sh
npm i aws-amplify --save
```
Once installed you see the dependencies installed in the Package.json
![dependencies in package.json](https://user-images.githubusercontent.com/125069098/223259307-bef2682d-a6a2-4be4-ad0d-9257ad1b5d91.png)

## Configure Amplify

We need to hook up our cognito pool to our code in the `App.js`

```js
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
 // "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});

## Modify the code in frontend-react-js/pages/ `HomeFeedPage.js`
```js
import { Auth } from 'aws-amplify';

// set a state
const [user, setUser] = React.useState(null);

// check if we are authenicated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};

// check when the page loads if we are authenicated
React.useEffect(()=>{
  loadData();
  checkAuth();
}, [])
```
We'll want to pass user to the following components: in frontend-react-js/components/DesktopNavigation.js and DesktopSidebar.js

```js
<DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
<DesktopSidebar user={user} />
```
We'll rewrite `DesktopNavigation.js` so that it it conditionally shows links in the left hand column
on whether you are logged in or not.

Notice we are passing the user to ProfileInfo

```js
import './DesktopNavigation.css';
import {ReactComponent as Logo} from './svg/logo.svg';
import DesktopNavigationLink from '../components/DesktopNavigationLink';
import CrudButton from '../components/CrudButton';
import ProfileInfo from '../components/ProfileInfo';

export default function DesktopNavigation(props) {

  let button;
  let profile;
  let notificationsLink;
  let messagesLink;
  let profileLink;
  if (props.user) {
    button = <CrudButton setPopped={props.setPopped} />;
    profile = <ProfileInfo user={props.user} />;
    notificationsLink = <DesktopNavigationLink 
      url="/notifications" 
      name="Notifications" 
      handle="notifications" 
      active={props.active} />;
    messagesLink = <DesktopNavigationLink 
      url="/messages"
      name="Messages"
      handle="messages" 
      active={props.active} />
    profileLink = <DesktopNavigationLink 
      url="/@andrewbrown" 
      name="Profile"
      handle="profile"
      active={props.active} />
  }

  return (
    <nav>
      <Logo className='logo' />
      <DesktopNavigationLink url="/" 
        name="Home"
        handle="home"
        active={props.active} />
      {notificationsLink}
      {messagesLink}
      {profileLink}
      <DesktopNavigationLink url="/#" 
        name="More" 
        handle="more"
        active={props.active} />
      {button}
      {profile}
    </nav>
  );
}
```
We'll rewrite `DesktopSidebar.js` so that it conditionally shows components in case you are logged in or not.

```js
import './DesktopSidebar.css';
import Search from '../components/Search';
import TrendingSection from '../components/TrendingsSection'
import SuggestedUsersSection from '../components/SuggestedUsersSection'
import JoinSection from '../components/JoinSection'

export default function DesktopSidebar(props) {
  const trendings = [
    {"hashtag": "100DaysOfCloud", "count": 2053 },
    {"hashtag": "CloudProject", "count": 8253 },
    {"hashtag": "AWS", "count": 9053 },
    {"hashtag": "FreeWillyReboot", "count": 7753 }
  ]

  const users = [
    {"display_name": "Andrew Brown", "handle": "andrewbrown"}
  ]

  let trending;
  let suggested;
  let join;
  if (props.user) {
    trending = <TrendingSection trendings={trendings} />
    suggested = <SuggestedUsersSection users={users} />
  }else {
    join = <JoinSection />
  }

  return (
    <section>
      <Search />
      {trending}
      {suggested}
      {join}
      <footer>
        <a href="#">About</a>
        <a href="#">Terms of Service</a>
        <a href="#">Privacy Policy</a>
      </footer>
    </section>
  );
}
```
We'll update `ProfileInfo.js`

```js
import { Auth } from 'aws-amplify';

const signOut = async () => {
  try {
      await Auth.signOut({ global: true });
      window.location.href = "/"
  } catch (error) {
      console.log('error signing out: ', error);
  }
}
```
### After the modifing the code check whether the app is working or not

![image](https://user-images.githubusercontent.com/125069098/223280420-43c07890-dcb5-4a41-96c8-e185cec13739.png)

## Signin Page

```js
import { Auth } from 'aws-amplify';

const [cognitoErrors, setCognitoErrors] = React.useState('');

const onsubmit = async (event) => {
  setCognitoErrors('')
  event.preventDefault();
     Auth.signIn(username, password)
      .then(user => {
        localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
        window.location.href = "/"
      })
      .catch(err => {  
         if (error.code == 'UserNotConfirmedException') {
           window.location.href = "/confirm"
         }
    setCognitoErrors(error.message)
  });
  return false
}

let errors;
if (cognitoErrors){
  errors = <div className='errors'>{cognitoErrors}</div>;
}

// just before submit component
{errors}
```
![signin](https://user-images.githubusercontent.com/125069098/223282552-d0b83827-3575-4327-b5fe-05f5b6f3ea37.png)

### Create a user in the aws cognito
Create a user in the cognito cruddur-user-pool
Use the same credentials to signin the cruddur app signin
signin with the username and password in the cruddur app signin
![image](https://user-images.githubusercontent.com/125069098/223285005-37c8047b-e52d-421a-b24e-15454f7b5a82.png)

### Force change password
 In we can do this by using aws-cli command
 
 ```aws-cli
 aws cognito-idp admin-set-user-password \
  --user-pool-id <your-user-pool-id> \
  --username <username> \
  --password <password> \
  --permanent
  ```
 
![sign in app](https://user-images.githubusercontent.com/125069098/223477034-1852c166-5636-47ae-bdae-f9683c80260f.png)

![image](https://user-images.githubusercontent.com/125069098/223481892-b4155325-9ac2-4757-91b8-a27b55ea70fd.png)
## Signup Page

```js
import { Auth } from 'aws-amplify';

const [cognitoErrors, setCognitoErrors] = React.useState('');

const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
            name: name,
            email: email,
            preferred_username: username,
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
            enabled: true,
        }
      });
      console.log(user);
      window.location.href = `/confirm?email=${email}`
  } catch (error) {
      console.log(error);
      setErrors(error.message)
  }
  return false
}

let errors;
if (cognitoErrors){
  errors = <div className='errors'>{cognitoErrors}</div>;
}

//before submit component
{errors}
```

## Confirmation Page

```js
const resend_code = async (event) => {
  setErrors('')
  try {
    await Auth.resendSignUp(email);
    console.log('code resent successfully');
    setCodeSent(true)
  } catch (err) {
    // does not return a code
    // does cognito always return english
    // for this to be an okay match?
    console.log(err)
    if (err.message == 'Username cannot be empty'){
      setErrors("You need to provide an email in order to send Resend Activiation Code")   
    } else if (err.message == "Username/client id combination not found."){
      setErrors("Email is invalid or cannot be found.")   
    }
  }
}

const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
    await Auth.confirmSignUp(email, code);
    window.location.href = "/"
  } catch (error) {
    setErrors(error.message)
  }
  return false
}
```


![signup confirmation page](https://user-images.githubusercontent.com/125069098/223499570-515ef0f9-7bb3-4462-9e92-df3ae6fe6574.png)
![cognito user exist](https://user-images.githubusercontent.com/125069098/223500593-08874920-4826-405c-af1c-f4e33b10e00e.png)
![signin app](https://user-images.githubusercontent.com/125069098/223501988-66a6f97c-ad9d-410e-88b4-fef51662f3e0.png)

## Recovery Page

```js
import { Auth } from 'aws-amplify';

const onsubmit_send_code = async (event) => {
  event.preventDefault();
  setCognitoErrors('')
  Auth.forgotPassword(username)
  .then((data) => setFormState('confirm_code') )
  .catch((err) => setCognitoErrors(err.message) );
  return false
}

const onsubmit_confirm_code = async (event) => {
  event.preventDefault();
  setCognitoErrors('')
  if (password == passwordAgain){
    Auth.forgotPasswordSubmit(username, code, password)
    .then((data) => setFormState('success'))
    .catch((err) => setCognitoErrors(err.message) );
  } else {
    setCognitoErrors('Passwords do not match')
  }
  return false
}
```

![recovery page](https://user-images.githubusercontent.com/125069098/223503949-15492caa-de4c-4cd4-bf51-aeb8752ccd4f.png)
![recovery confirmation](https://user-images.githubusercontent.com/125069098/223504594-c33d436f-3905-4f0b-a404-43e3484c6d4c.png)
![signin](https://user-images.githubusercontent.com/125069098/223505142-755a1913-a3de-4e34-9843-a68de5234082.png)

## Forgot password
![forgot password](https://user-images.githubusercontent.com/125069098/224359888-62d6152e-cea0-4bb4-b01e-9272e4650b68.png)
![recovery password](https://user-images.githubusercontent.com/125069098/224360521-8fbcd7e8-46e8-4812-85b8-999fb62511d4.png)
![success recovery password](https://user-images.githubusercontent.com/125069098/224360751-d9d95184-0b62-4729-b4c7-8845e26757b1.png)

## Authenticating Server Side

Add in the `HomeFeedPage.js` a header to pass along the access token

```js
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`
  }
```

In the `app.py`

```py
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
```
Add a Flask-AWSCognito to the requirements.txt in the backend-flask folder

```py
pip install -r requirements.txt
```

In the create a new file to validate the JWT in backend-flask folder/lib/cognito_jwt_token.py
```py
import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode
class FlaskAWSCognitoError(Exception):
  pass
class TokenVerifyError(Exception):
  pass
def extract_access_token(request_headers):
     
    access_token = None
    auth_header = request_headers.get("Authorization")
    if auth_header and " " in auth_header:
        _, access_token = auth_header.split()
    return access_token  

class CognitoJwtToken:
  
  def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
    self.region = region
    if not self.region:
        raise FlaskAWSCognitoError("No AWS region provided")
    self.user_pool_id = user_pool_id
    self.user_pool_client_id = user_pool_client_id
    self.claims = None
    if not request_client:
        self.request_client = requests.get
    else:
        self.request_client = request_client
    self._load_jwk_keys()

  def _load_jwk_keys(self):
    keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
    #keys_url = f"https://cognito-idp.<region>.amazonaws.com/<poolid>/.well-known/jwks.json" 
    try:
      response = self.request_client(keys_url)
      self.jwk_keys = response.json()["keys"]
    except requests.exceptions.RequestException as e:
      raise FlaskAWSCognitoError(str(e)) from e

  @staticmethod
  def _extract_headers(token):
    try:
        headers = jwt.get_unverified_headers(token)
        return headers
    except JOSEError as e:
        raise TokenVerifyError(str(e)) from e

  def _find_pkey(self, headers):
    kid = headers["kid"]
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(self.jwk_keys)):
        if kid == self.jwk_keys[i]["kid"]:
            key_index = i
            break
    if key_index == -1:
        raise TokenVerifyError("Public key not found in jwks.json")
    return self.jwk_keys[key_index]

  @staticmethod
  def _verify_signature(token, pkey_data):
    try:
        # construct the public key
        public_key = jwk.construct(pkey_data)
    except JOSEError as e:
        raise TokenVerifyError(str(e)) from e
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit(".", 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        raise TokenVerifyError("Signature verification failed")

  @staticmethod
  def _extract_claims(token):
    try:
        claims = jwt.get_unverified_claims(token)
        return claims
    except JOSEError as e:
        raise TokenVerifyError(str(e)) from e

  @staticmethod
  def _check_expiration(claims, current_time):
    if not current_time:
        current_time = time.time()
    if current_time > claims["exp"]:
        raise TokenVerifyError("Token is expired")  # probably another exception

  def _check_audience(self, claims):
    # and the Audience  (use claims['client_id'] if verifying an access token)
    audience = claims["aud"] if "aud" in claims else claims["client_id"]
    if audience != self.user_pool_client_id:
        raise TokenVerifyError("Token was not issued for this audience")

  def verify(self, token, current_time=None):
    """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
    if not token:
        raise TokenVerifyError("No token provided")
    headers = self._extract_headers(token)
    pkey_data = self._find_pkey(headers)
    self._verify_signature(token, pkey_data)
    claims = self._extract_claims(token)
    self._check_expiration(claims, current_time)
    self._check_audience(claims)
    self.claims = claims
    return claims
```
Modify the code in the **app.py** in backend-flask folder

```py
#Authorization JWT
from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError

app = Flask(__name__)

# Authorization JWT
cognito_jwt_token = CognitoJwtToken(
  user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"), 
  user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region=os.getenv("AWS_DEFAULT_REGION")
)

@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture('activities_home')
def data_home():
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    # authenicatied request
    app.logger.debug("authenicated")
    app.logger.debug(claims)
    app.logger.debug(claims['username'])
    data = HomeActivities.run(cognito_user_id=claims['username'])
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    app.logger.debug("unauthenicated")
    data = HomeActivities.run()
  return data, 200
```
Modify the code in **docker-compose.yml** to include the environments
```docker
      AWS_COGNITO_USER_POOL_ID: "ca-central-1_CQ4wDfnwc"
      AWS_COGNITO_USER_POOL_CLIENT_ID: "5b6ro31g97urk767adrbrdj1g5"
 ```
 
 Modify the code in the **Home_Activities.py** in backend-flask folder
 
 ```py
 class HomeActivities:
  def run(cognito_user_id=None):
    # Logger.info("HomeActivities")
    
  if cognito_user_id != None:
        extra_crud = {
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Lore',
          'message': 'My dear brother, it the humans that are the problem',
          'created_at': (now - timedelta(hours=1)).isoformat(),
          'expires_at': (now + timedelta(hours=12)).isoformat(),
          'likes': 1042,
          'replies': []
        }
        results.insert(0,extra_crud)
```     
![signin](https://user-images.githubusercontent.com/125069098/224725849-a5bec431-404b-4b84-97fc-cfa34a094329.png)

Modify the code in the **ProfileInfo.py**

```py
const signOut = async () => {
    try {
        await Auth.signOut({ global: true });
        window.location.href = "/"
        localStorage.removeItem("access_token")
    } catch (error) {
        console.log('error signing out: ', error);
    }
  }
```  
![signout](https://user-images.githubusercontent.com/125069098/224725972-7b6cbd25-48c4-4b56-8414-e36dc21e46a9.png)



