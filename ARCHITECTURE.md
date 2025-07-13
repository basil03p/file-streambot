# FileStreamBot Architecture Documentation

## Multi-Bot System Architecture

### Overview
The FileStreamBot implements a **single main bot + multiple backend processors** architecture to boost performance while maintaining a clean user experience.

### Architecture Components

#### 1. Main Bot (User Interface)
- **Purpose**: Handles ALL user interactions
- **Responsibilities**:
  - Receives user messages and commands
  - Sends responses to users
  - Manages user interface and conversations
  - Handles authorization and authentication
  - Manages user requests and rate limiting

#### 2. Backend Processing Bots
- **Purpose**: Handle backend file processing tasks only
- **Responsibilities**:
  - File downloading and processing
  - File ID generation and storage
  - Heavy computational tasks
  - Load distribution for speed boost

#### 3. Request Management System
- **Features**:
  - One active request per user at a time
  - 5-minute timeout for incomplete requests
  - Revoke/cancel functionality via `/revoke` command
  - Request status tracking

#### 4. File Expiration System
- **Automatic Cleanup**: Files deleted from database after 1 hour
- **Background Tasks**: Periodic cleanup of expired files and old requests
- **User Notifications**: Clear expiration warnings

### Bot Interaction Flow

#### User File Upload (Private Messages)
```
1. User sends file → Main Bot
2. Main Bot validates request and user
3. Main Bot selects least loaded Backend Bot for processing
4. Backend Bot handles file operations (get_file_ids, etc.)
5. Main Bot sends response to user with download links
6. Main Bot updates request status
```

#### Channel File Processing
```
1. File posted in channel → Main Bot receives
2. If authorized channel: Backend Bot processes file for speed
3. Main Bot edits message with download buttons
4. All user interactions still go through Main Bot
```

### Configuration

#### Environment Variables
```bash
# Multi-bot configuration
MULTI_BOT_MODE=True
MULTI_TOKENS="token1,token2,token3"  # Backend bot tokens
BOT_TOKEN="main_bot_token"          # Main bot token

# Optional features
AUTH_CHANNEL="-1001234567890"       # Authorized channel ID
GENERATE_DOWNLOAD_LINKS=True        # Enhanced features for auth channel
```

### Key Benefits

1. **Performance**: Backend bots handle heavy processing
2. **User Experience**: Single consistent interface (main bot)
3. **Scalability**: Add more backend bots as needed
4. **Reliability**: Fallback to main bot if backends unavailable
5. **Load Distribution**: Automatic load balancing across backend bots

### Implementation Details

#### Main Bot Responsibilities
- All user message handlers (`@FileStream.on_message`)
- All user responses and notifications
- Request validation and rate limiting
- Authentication and authorization

#### Backend Bot Usage
- File processing operations only
- No direct user interaction
- Load-balanced selection for optimal performance
- Automatic failover to main bot if needed

### Security Considerations

1. **Token Security**: Backend tokens should be kept separate and secure
2. **User Privacy**: Only main bot has access to user data
3. **Channel Authorization**: Strict validation for authorized channels
4. **Request Isolation**: Users cannot interfere with each other's requests

### Monitoring and Logging

- Bot performance statistics
- Load balancing metrics
- Request tracking and completion rates
- Error handling and fallback mechanisms

This architecture ensures optimal performance while maintaining security and user experience consistency.
