from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HighScore
import json

def index(request):
    """Render the main HTML5/JavaScript Dino Runner page."""
    return render(request, "game/index.html")

@csrf_exempt
def save_score(request):
    """AJAX POST endpoint to save the player's score to the database."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            player_name = data.get("player_name", "Anonymous").strip()
            score = int(data.get("score", 0))
            
            if not player_name:
                player_name = "Anonymous"
                
            high_score = HighScore.objects.create(player_name=player_name, score=score)
            return JsonResponse({
                "status": "success",
                "player_name": high_score.player_name,
                "score": high_score.score
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def leaderboard(request):
    """AJAX GET endpoint to fetch the top 10 scores."""
    top_scores = HighScore.objects.all()[:10]
    scores_list = [
        {
            "player_name": hs.player_name,
            "score": hs.score,
            "date": hs.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for hs in top_scores
    ]
    return JsonResponse({"status": "success", "leaderboard": scores_list})
