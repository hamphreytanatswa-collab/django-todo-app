# from django.shortcuts import redirect, get_object_or_404
# from django.views.generic import ListView, CreateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Todo
# from .forms import TodoForm
# from django.views.generic import UpdateView

# class TodoListView(LoginRequiredMixin, ListView):
#     model = Todo
#     template_name = 'todos/todo_list.html'
#     context_object_name = 'todos'
#     def get_queryset(self):
#         return Todo.objects.filter(user=self.request.user)

# class TodoUpdateView(LoginRequiredMixin, UpdateView):
#     model = Todo
#     form_class = TodoForm
#     template_name = 'todos/todo_form.html'
#     success_url = reverse_lazy('todo_list')

# class TodoCreateView(LoginRequiredMixin, CreateView):
#     model = Todo
#     form_class = TodoForm
#     template_name = 'todos/todo_form.html'
#     success_url = reverse_lazy('todo_list')
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

# class TodoDeleteView(LoginRequiredMixin, DeleteView):
#     model = Todo
#     template_name = 'todos/todo_confirm_delete.html'
#     success_url = reverse_lazy('todo_list')

# def toggle_todo(request, pk):
#     todo = get_object_or_404(Todo, pk=pk)
#     todo.completed = not todo.completed
#     todo.save()
#     return redirect('todo_list')

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Todo
from .forms import TodoForm

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        # Only show tasks belonging to the logged-in user
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Get the original context (which contains our 'todos' list)
        context = super().get_context_data(**kwargs)
        
        # Calculate progress
        todos = self.get_queryset()
        total_tasks = todos.count()
        completed_tasks = todos.filter(completed=True).count()
        
        # Prevent division by zero if the list is empty
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Add the 'progress' variable to the context to use in the HTML
        context['progress'] = round(progress, 1)
        return context

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')
    
    def form_valid(self, form):
        # Automatically assign the logged-in user to the new task
        form.instance.user = self.request.user
        return super().form_valid(form)

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')

def toggle_todo(request, pk):
    # This remains a functional view for a quick state toggle
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')