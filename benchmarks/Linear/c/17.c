
int main()
{
    int x = 1;
    int m = 1;
    int n;

    while (x < n) {
        if (unknown()) {
            m = x;
        }
        x = x + 1;
    }

    //post-condition
    if(n > 1) {
       assert (m < n);
       //assert (m >= 1);
    }
}
//
branch 1 : n < 1
branch 2 : n >= 1 and unknown() == true
branch 3 : n >= 1 and unknown() == false
