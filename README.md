# SSL Certificate Checker

A modern web application that allows users to check SSL certificates for any domain. Built with Flask and featuring a clean, responsive UI using Tailwind CSS.

![SSL Checker Screenshot](https://via.placeholder.com/800x400.png?text=SSL+Checker+Screenshot)

## Features

### Core Functionality
- Check SSL certificates for any domain
- View detailed certificate information
- Certificate health score calculation
- Visual timeline of certificate validity
- Security recommendations
- Technical certificate details

### User Features
- User authentication (signup/login)
- Personal SSL check history
- Secure password handling
- User-specific data isolation

### Technical Features
- Modern, responsive UI with Tailwind CSS
- Real-time certificate validation
- Persistent storage of check history
- Docker containerization
- Database integration (SQLite)
- RESTful API endpoints

## Technology Stack

- **Backend**: Python/Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: Flask-Login
- **Container**: Docker
- **API**: RapidAPI SSL Checker

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- RapidAPI Key (for SSL checking service)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ssl-checker.git
cd ssl-checker
```

2. Create a `.env` file:
```bash
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
RAPIDAPI_KEY=your-rapidapi-key-here
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Access the application at `http://localhost:5000`

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here
export RAPIDAPI_KEY=your-rapidapi-key-here
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

## Usage

1. Create an account or log in
2. Enter a domain name in the check form
3. View the SSL certificate details:
   - Certificate validity status
   - Expiration date
   - Days remaining
   - Health score
   - Security recommendations
   - Technical details

## API Endpoints

- `POST /check_ssl`: Check SSL certificate for a domain
- `GET /history`: Get SSL check history for the current user
- `POST /signup`: Create a new user account
- `POST /login`: Authenticate user
- `GET /logout`: Log out current user

## Security Features

- Password hashing using bcrypt
- Session-based authentication
- CSRF protection
- Secure password storage
- Input validation and sanitization

## Database Schema

### User Model
```python
class User:
    id: Integer (Primary Key)
    email: String (Unique)
    password_hash: String
    name: String
    created_at: DateTime
```

### SSLCheck Model
```python
class SSLCheck:
    id: Integer (Primary Key)
    domain: String
    check_date: DateTime
    is_valid: Boolean
    expiry_date: DateTime
    issuer: String
    user_id: Integer (Foreign Key)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- RapidAPI for the SSL checking service
- Tailwind CSS for the UI framework
- Flask community for the excellent web framework
- All contributors and users of the application

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add support for bulk certificate checking
- [ ] Implement email notifications for expiring certificates
- [ ] Add certificate renewal reminders
- [ ] Integrate with more SSL checking services
- [ ] Add support for custom SSL checker configurations
- [ ] Implement API key management for users
- [ ] Add export functionality for check results 