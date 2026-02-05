const Database = require('better-sqlite3');
const crypto = require('crypto');

// Hash password using same method as Better Auth
function hashPassword(password) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

const db = new Database('./auth.db');

// Create tables if they don't exist
db.exec(`
    CREATE TABLE IF NOT EXISTS user (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        emailVerified INTEGER DEFAULT 0,
        name TEXT,
        createdAt INTEGER NOT NULL,
        updatedAt INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS account (
        id TEXT PRIMARY KEY,
        userId TEXT NOT NULL,
        accountId TEXT NOT NULL,
        providerId TEXT NOT NULL,
        accessToken TEXT,
        refreshToken TEXT,
        idToken TEXT,
        expiresAt INTEGER,
        password TEXT,
        createdAt INTEGER NOT NULL,
        updatedAt INTEGER NOT NULL,
        FOREIGN KEY (userId) REFERENCES user(id)
    );
`);

const userId = crypto.randomUUID();
const accountId = crypto.randomUUID();
const now = Date.now();

const email = 'test@example.com';
const password = 'password123';
const hashedPassword = hashPassword(password);

try {
    // Insert user
    const insertUser = db.prepare(`
        INSERT INTO user (id, email, emailVerified, name, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?)
    `);

    insertUser.run(userId, email, 1, 'Test User', now, now);

    // Insert account with password
    const insertAccount = db.prepare(`
        INSERT INTO account (id, userId, accountId, providerId, password, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `);

    insertAccount.run(accountId, userId, email, 'credential', hashedPassword, now, now);

    console.log('✅ Test user created successfully!');
    console.log('');
    console.log('=== LOGIN CREDENTIALS ===');
    console.log('Email:    test@example.com');
    console.log('Password: password123');
    console.log('=========================');
} catch (error) {
    if (error.message.includes('UNIQUE constraint failed')) {
        console.log('ℹ️  User already exists!');
        console.log('');
        console.log('=== LOGIN CREDENTIALS ===');
        console.log('Email:    test@example.com');
        console.log('Password: password123');
        console.log('=========================');
    } else {
        console.error('❌ Error:', error.message);
    }
}

db.close();
