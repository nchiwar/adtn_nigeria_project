import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";



// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  apiKey: "AIzaSyCW79Et5xKofKWYCiagpoAZKM7hRXpoxYs",
  authDomain: "dental-76f34.firebaseapp.com",
  projectId: "dental-76f34",
  storageBucket: "dental-76f34.firebasestorage.app",
  messagingSenderId: "167499697294",
  appId: "1:167499697294:web:b3cdcc51df3eb4e660cddf"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);


// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);

