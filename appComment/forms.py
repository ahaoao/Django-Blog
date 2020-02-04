import mistune
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """评论表单"""
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={
                'class': 'form-control',
                'style': 'width: 60%;',
            }
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 60%;',
            }
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 60%;',
            }
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={
                'rows': 6,
                'cols': 60,
                'class': 'form-control',
            }
        )
    )

    def clean_content(self):
        """控制评论的长度，太短直接抛出异常"""
        content = self.cleaned_data.get('content')
        content = mistune.markdown(content)
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么能这么短呢！')
        return content

    class Meta:
        model = Comment
        # 控制在网页显示的字段
        fields = ['nickname', 'email', 'website', 'content']
