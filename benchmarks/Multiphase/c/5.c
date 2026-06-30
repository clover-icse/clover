int main(){
    int x, y, z;

    // pre-conditions
    assume(x > 0);
    assume(y < 0);
    z = 1;

    // loop body
    while(unknown()){
        if(y >= 0){
            z = z * 2;
        }
        x = x + 1;
        y = y + 2;
    }

    // post-condition
    if(y >= x){
        assert(z > 1);
    }
    
}