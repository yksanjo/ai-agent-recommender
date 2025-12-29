# Changelog

## [2.0.0] - Enhanced Agentic Chatbot Redesign

### 🎉 Major Redesign

#### Enhanced Agent Intelligence
- **Advanced Reasoning**: New `EnhancedRecommenderAgent` with planning, reflection, and adaptive responses
- **Multi-Purpose**: Agent can now:
  - Discover existing agent use cases
  - Explain AI agent concepts and frameworks
  - Help users plan and build their own agents
- **Context Memory**: Maintains conversation history with checkpointing
- **Smart Suggestions**: Automatically generates relevant follow-up questions

#### Beautiful New UI
- **Modern Design**: Gradient-based theme with purple/blue colors
- **Smooth Animations**: Fade-in effects and hover transitions
- **Chat Interface**: Beautiful message bubbles with user/assistant styling
- **Interactive Cards**: Recommendation cards with hover effects
- **Two Modes**: 
  - 💬 Chat mode for conversations
  - 🔍 Quick Search for fast results
- **Better UX**: Improved layout, spacing, and visual hierarchy

#### New Features
- **Conversational API**: New `/api/chat` endpoint for enhanced chat
- **Thread Management**: Conversation threads for better context
- **Suggestion Chips**: Clickable follow-up suggestions
- **Enhanced Recommendations**: Better formatting and display
- **Export Functionality**: Download recommendations as JSON

### Technical Improvements
- Better error handling and fallbacks
- Improved import compatibility
- Enhanced API responses with structured data
- Better state management in UI

### Migration Notes
- Old UI still available at `web/app.py`
- New enhanced UI at `web/enhanced_app.py`
- Use `streamlit run web/enhanced_app.py` for new experience
- API now supports both old and new endpoints

## [1.0.0] - Initial Release

- Basic recommender agent
- CLI interface
- Web UI (original)
- REST API
- Vector search with ChromaDB

