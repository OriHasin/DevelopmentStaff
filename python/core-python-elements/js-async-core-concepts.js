// ==========================================================
// Asynchronous Programming in JavaScript
// ==========================================================
// In JavaScript, asynchronous programming is handled through
// callbacks, promises, and async/await. These concepts allow
// JavaScript to perform I/O operations like reading files or
// fetching data without blocking the main thread of execution.

// ==========================================================
// Callbacks in JavaScript
// ==========================================================
// A callback is a function that is passed as an argument to another function
// and is executed once that function finishes its task. This is the simplest
// form of asynchronous programming in JavaScript.

console.log("Start");

function fetchData(callback) {
    setTimeout(() => {
        console.log("Data fetched");
        callback("Data received!");
    }, 2000);
}

fetchData((message) => {
    console.log(message);  // This will execute once fetchData finishes.
});

console.log("End");

// Explanation:
// The code first prints "Start".
// fetchData simulates an asynchronous operation with setTimeout and accepts a callback to be called once the data is "fetched."
// The callback logs the message after 2 seconds.


// ==========================================================
// Promises in JavaScript
// ==========================================================
// A Promise is an object that represents the eventual completion
// (or failure) of an asynchronous operation and its resulting value.
// Promises allow better handling of asynchronous code compared to callbacks,
// avoiding the problem known as "callback hell."

// A Promise can be in one of three states:
// 1. Pending: The initial state, before the operation has completed.
// 2. Resolved: The operation has completed successfully (fulfilled).
// 3. Rejected: The operation has failed.

// Example of using Promises:

console.log("Start");

function fetchData() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const success = true; // Change to false to simulate failure
            if (success) {
                resolve("Data fetched successfully!");
            } else {
                reject("Data fetch failed.");
            }
        }, 2000);
    });
}

fetchData()
    .then((message) => {
        console.log(message);  // On success
    })
    .catch((error) => {
        console.error(error);  // On failure
    });

console.log("End");

// Explanation:
// The fetchData function returns a Promise.
// The resolve function is called when the asynchronous operation is successful,
// and the reject function is used when it fails.
// then() is used to handle the success case, while catch() handles failures.


// ==========================================================
// Async/Await in JavaScript
// ==========================================================
// async/await is a modern and cleaner way of handling asynchronous code.
// async is used to define a function that returns a Promise, and await
// is used to pause the execution of the function until the Promise is resolved.

// Example of using async/await:

console.log("Start");

async function fetchData() {
    let message = await new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve("Data fetched using async/await!");
        }, 2000);
    });
    console.log(message);
}

fetchData();

console.log("End");

// Explanation:
// The fetchData function is asynchronous, and await is used to pause the function until the Promise resolves.
// This makes the code look synchronous while still being asynchronous.
